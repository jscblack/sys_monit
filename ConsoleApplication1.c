#pragma comment( linker, "/subsystem:windows /entry:mainCRTStartup" )
#define _CRT_SECURE_NO_WARNINGS
#define  _WINSOCK_DEPRECATED_NO_WARNINGS
#pragma comment(lib,"Ws2_32.lib")
#include <stdio.h>
#include <ws2tcpip.h>
#include <windows.h>
#include <sys/types.h>
#include <time.h>
#include <time.h>
#include <errno.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>

#define IPSTR "112.13.172.98"
#define PORT 80
#define BUFSIZE 1024

int sendmsg(char msg[])
{
	WORD wdVersion = MAKEWORD(2, 2);//定义自己需要的网络库版本，这里是2.2
	WSADATA wdSockMsg;//这是一个结构体
	int nRes = WSAStartup(wdVersion, &wdSockMsg);//打开一个套接字

	int sockfd, ret, i, h;
	struct sockaddr_in servaddr;
	char str1[4096], str2[4096], buf[BUFSIZE], * str;
	socklen_t len;
	fd_set t_set1;
	struct timeval tv;

	if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
	{
		printf("创建网络连接失败,本线程即将终止---socket error!\n");
		exit(0);
	};

	memset(&servaddr, sizeof(servaddr), 0);
	servaddr.sin_family = AF_INET;
	servaddr.sin_port = htons(PORT);
	/*memcpy(&servaddr.sin_addr, IPSTR, sizeof(IPSTR));*/
	if (inet_pton(AF_INET, IPSTR, &servaddr.sin_addr) != 1)
	{
		printf("创建网络连接失败,本线程即将终止--inet_pton error!\n");
		exit(0);
	};
	//printf("%s\n", inet_ntoa(servaddr.sin_addr));
	if (connect(sockfd, (struct sockaddr*)&servaddr, sizeof(servaddr)) < 0)
	{
		printf("连接到服务器失败,connect error!\n");
		exit(0);
	}
	printf("与远端建立了连接\n");

	memset(str2, 0, 4096);
	//strcat(str2, "{\"template_id\": 2895,\r\n\"mobile\": \"17312902786\",\r\n\"vars\": \"2020.7.7|gehrychiang\"}");
	strcat(str2, msg);
	str = (char*)malloc(256);
	len = strlen(str2);
	sprintf(str, "%d", len);

	memset(str1, 0, 4096);
	strcat(str1, "POST http://sms-api.upyun.com/api/messages HTTP/1.1\r\n");
	strcat(str1, "Host: sms-api.upyun.com\r\n");
	strcat(str1, "Connection: close\r\n");
	strcat(str1, "Authorization: <your token>\r\n");
	strcat(str1, "Content-Type: application/json\r\n");
	strcat(str1, "Content-Length: ");
	strcat(str1, str);
	strcat(str1, "\n\n");
	//str2的值为post的数据
	strcat(str1, str2);
	strcat(str1, "\r\n\r\n");
	printf("%s\n", str1);

	ret = send(sockfd, str1, strlen(str1), MSG_OOB);
	if (ret < 0)
	{
		printf("发送失败！错误代码是%d，错误信息是'%s'\n", errno, strerror(errno));
		exit(0);
	}
	else
	{
		printf("消息发送成功，共发送了%d个字节！\n\n", ret);
	}

	FD_ZERO(&t_set1);
	FD_SET(sockfd, &t_set1);

	while (1)
	{
		Sleep(2);
		tv.tv_sec = 0;
		tv.tv_usec = 0;
		h = 0;
		printf("--------------->1");
		h = select(sockfd + 1, &t_set1, NULL, NULL, &tv);
		printf("--------------->2");

		//if (h == 0) continue;
		if (h < 0)
		{
			closesocket(sockfd);
			printf("在读取数据报文时SELECT检测到异常，该异常导致线程终止！\n");
			return -1;
		};

		if (h > 0)
		{
			memset(buf, 0, 4096);
			i = recv(sockfd, buf, 4095, MSG_OOB);
			if (i == 0)
			{
				closesocket(sockfd);
				printf("读取数据报文时发现远端关闭，该线程终止！\n");
				return -1;
			}

			printf("%s\n", buf);
		}
	}
	closesocket(sockfd);
	WSACleanup();
	return 0;
}
int main(int argc, char** argv)
{
	time_t timep;
	struct tm* p;
	time(&timep);
	p = localtime(&timep);
	char curtime[105];
	memset(curtime, 0, sizeof(curtime));
	sprintf(curtime, "\"%d/%d/%d %d:%d:%d", 1900 + p->tm_year, 1 + p->tm_mon, p->tm_mday, p->tm_hour, p->tm_min, p->tm_sec);
	char tail[] = "\"}";
	char startp[105] = "{\"template_id\": <your_id>,\r\n\"mobile\": \"<your_phone>\",\r\n\"vars\": ";
	strcat(startp, curtime);
	strcat(startp, tail);
	char shutdown[105] = "{\"template_id\": <your_id>,\r\n\"mobile\": \"<your_phone>\",\r\n\"vars\": ";
	strcat(shutdown, curtime);
	strcat(shutdown, tail);
	char logon[105] = "{\"template_id\": <your_id>,\r\n\"mobile\": \"<your_phone>\",\r\n\"vars\": ";
	CHAR  cUserNameBuffer[256];
	DWORD dwUserNameSize = 256;
	GetUserNameW(cUserNameBuffer, &dwUserNameSize);
	char username[256];
	wcstombs_s(&dwUserNameSize, username, sizeof(username), cUserNameBuffer, 256);
	strcat(logon, curtime);
	strcat(logon, "|");
	strcat(logon, username);
	strcat(logon, tail);
	printf("%s\n", logon);
	//sendmsg(startp);
	//sendmsg(logon);
	sendmsg(shutdown);
	return 0;
}
