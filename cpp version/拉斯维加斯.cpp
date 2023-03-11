#include <iostream>
#include <math.h>
#include <ctime>
#include <algorithm>
#include <vector>
using namespace std;
typedef long long ll;
const int users = 76;
const int start_number = 8;
const int wrong = 65536;
class chess
{
public:
    ll money;
    int pieces_number[users];
    bool visited; //定义访问值，判断是否有人投资这个棋盘
    chess()
    { //将每个人棋盘上对应的棋子个数都重置为0，每个数组格子对应一个玩家
        this->money = (rand() % 10 + 1) * 10e3;
        for (int i = 0; i < users; i++)
        {
            pieces_number[i] = 0;
        }
        visited = false;
    }
    bool find_repeat(int data)
    { //查重函数，看看是否有对冲现象
        int count = 0;
        for (int i = 0; i < users; i++)
        {
            if (pieces_number[i] == data)
                count++;
        }
        if (count > 1)
            return true;
        else
            return false;
    }
    bool find_same()
    { //考虑极端情况，所有人都对冲
        int temp = pieces_number[0];
        for (int i = 0; i < users; i++)
        {
            if (pieces_number[i] != temp)
                return false;
        }
        return true;
    }
    int findmax() //找到每轮游戏每个棋盘上最终赢家
    {
        if (!visited)
        {
            return wrong;
        }
        int temp = pieces_number[0];
        int sequence = 0;
        for (int i = 1; i < users; i++)
        {
            if (temp < pieces_number[i])
            { //找到最大值
                temp = pieces_number[i];
                sequence = i;
            }
        }
        if (find_same())
        {
            return wrong;
        }
        if (!find_repeat(temp))
        {
            return sequence;
        }
        else
        {
            for (int i = 0; i < users; i++)
            {
                if (pieces_number[i] == temp)
                {
                    pieces_number[i] = 0;
                }
            }
            return findmax();
        }
    }
    void change(int sequence, int number)
    {                                      //玩家投资骰子个数
        pieces_number[sequence] += number; //把玩家投资的骰子个数放到棋盘上
        visited = true;
    }
};
class player
{
public:
    int sequence; //每个玩家的编号
    int number;   //骰子个数
    ll own_money; //已经拥有的钱数

    player()
    {
        this->number = start_number;
        this->own_money = 0;
    }
};
vector<int> get_number(int rest_number) //抛骰子的过程
{
    vector<int> record(users, 0); //定义一个长度为6的数组，记录每次抛骰子上每个点数的个数
    for (int i = 0; i < rest_number; i++)
    {
        int a = rand() % 6 + 1;
        record[a - 1]++;
    }
    return record;
}
bool finish(player players[])
{ //判断一轮游戏是否结束
    for (int i = 0; i < users; i++)
    {
        if (players[i].number != 0)
            return false;
    }
    return true;
}
int main()
{
    srand(time(nullptr));
    chess chessboard[6];
    player players[users];
    for (int i = 0; i < users; i++)
    { //给玩家们排上序号
        players[i].sequence = i;
    }
    cout << "欢迎来到拉斯维加斯赌场!" << endl;
    for (int i = 0; i < 6; i++)
    {
        cout << "第" << i + 1 << "个棋盘赌注为:" << chessboard[i].money << endl;
    }
    while (!finish(players)) //一轮游戏从每人8个棋子开始，到所有人棋子都在棋盘上结束
    {
        for (int i = 0; i < 6; i++)
        {
            cout << endl;
            cout << "请玩家" << players[i].sequence + 1 << "开始游戏,你的抛骰子结果为:" << endl;
            if (players[i].number == 0)
            { //已经没有棋子数了
                cout << "已经没有棋子数了" << endl;
                continue;
            }
            vector<int> result = get_number(players[i].number);
            for (int i = 0; i < result.size(); i++)
            {
                for (int j = 0; j < result[i]; j++)
                {
                    cout << i + 1 << " ";
                }
            }
            cout << endl;
            int choice;
            cout << "请输入你要投注的棋盘: ";
            cin >> choice;
        flag:
            if (result[choice - 1] != 0)
            {
                chessboard[choice - 1].change(players[i].sequence, result[choice - 1]); //棋盘上添加棋子
                players[i].number -= result[choice - 1];                                //玩家手里减少棋子
                cout << choice << "号棋盘上增加" << players[i].sequence + 1 << "号玩家" << result[choice - 1] << "枚骰子" << endl;
                //在每一小轮每个玩家投注后，显示现在每个投注盘上每个玩家的骰子数量
                cout << "**********************************" << endl;
                cout << "棋盘信息:" << endl;
                for (int i = 0; i < 6; i++)
                {
                    cout << endl;
                    cout << "第" << i + 1 << "个棋盘赌注为:" << chessboard[i].money << endl;
                    for (int j = 0; j < users; j++)
                    {
                        if (chessboard[i].pieces_number[j] != 0)
                        {
                            cout << "第" << j + 1 << "号玩家" << chessboard[i].pieces_number[j] << "个"
                                 << " ";
                        }
                    }
                    cout << endl;
                }
                cout << "**********************************" << endl;
            }
            else
            {
                cout << "错误！，请重新输入你要投注的棋盘：";
                cin >> choice;
                goto flag;
            }
        }
    }
    int winner[6];
    for (int i = 0; i < 6; i++)
    { //结算界面，找到棋盘上每一轮的赢家
        winner[i] = chessboard[i].findmax();
    }
    cout << endl;
    for (int i = 0; i < 6; i++)
    {
        if(winner[i]!=wrong)
            cout << "棋盘上" << i + 1 << "号的赢家为" << winner[i] + 1 << "号玩家,获得" << chessboard[i].money << "元" << endl;
        else
            cout<< i+1 << "号棋盘由于对冲或无人投资失效" << endl;
    }
    cout << "**********************************" << endl;
    cout << "这一轮的棋盘信息:" << endl;
    for (int i = 0; i < 6; i++)
    {
        cout << endl;
        cout << "第" << i + 1 << "个棋盘赌注为:" << chessboard[i].money << endl;
        for (int j = 0; j < users; j++)
        {
            if (chessboard[i].pieces_number[j] != 0)
            {
                cout << "第" << j + 1 << "号玩家" << chessboard[i].pieces_number[j] << "个"
                     << " ";
            }
        }
        cout << endl;
    }
    cout << "**********************************" << endl;
}