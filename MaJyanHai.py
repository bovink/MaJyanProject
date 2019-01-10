# 牌的类别为筒，万，索，字牌
# 筒，万，索的数字就从1到9，字牌的顺序为东南西北白发中
import math


class Hai:

    def __init__(self, name):
        self.name = name
        self.num = int(name[0])
        self.type = name[1]

    def next(self):
        if self.type in ['p', 'm', 's']:
            if self.num == 9:
                nextNum = 1
            else:
                nextNum = self.num + 1
        else:
            if self.num == 4:
                nextNum = 1
            elif self.num == 7:
                nextNum = 5
            else:
                nextNum = self.num + 1

        l = ''
        l += str(nextNum)
        l += self.type
        return Hai(l)

    def getName(self):
        return self.name

    def previous(self):
        if self.type in ['p', 'm', 's']:
            if self.num == 1:
                nextNum = 9
            else:
                nextNum = self.num - 1
        else:
            if self.num == 1:
                nextNum = 4
            elif self.num == 5:
                nextNum = 7
            else:
                nextNum = self.num - 1

        l = ''
        l += str(nextNum)
        l += self.type
        return Hai(l)

    def print(self):
        print('hai is {}{}'.format(self.num, self.type))


class Dazi:

    def __init__(self, hai1: Hai, hai2: Hai):
        self.hai1 = hai1
        self.hai2 = hai2

    def isDazi(self):
        if self.hai1.num < self.hai2.num:
            min = self.hai1
            max = self.hai2
        else:
            min = self.hai2
            max = self.hai1

        if self.hai1.type in ['p', 'm', 's']:
            if max.num - min.num < 3:
                return True

        else:
            if max.num - min.num == 0:
                return True

        return False

    def need(self):
        if self.hai1.num < self.hai2.num:
            min = self.hai1
            max = self.hai2
        else:
            min = self.hai2
            max = self.hai1

        if self.hai1.type in ['p', 'm', 's']:
            if max.num - min.num == 2:
                min.next().print()

            if max.num - min.num == 1:
                if min.num == 1:
                    max.next().print()
                elif max == 9:
                    min.previous().print()
                else:
                    min.previous().print()
                    max.next().print()

            if max.num - min.num == 0:
                min.print()
        else:
            if max.num - min.num == 0:
                min.print()


# 4个面子1个雀头 面子可为顺子或者刻子
# 如果所有牌都不搭，按一般形来做牌的话，即一张浮牌需要摸进2次有效自摸才能形成面子，那4个面子即需要8次有效自摸即可形成单吊听牌

class TeHai:

    def __init__(self, tehai: list = None, tehaistr: str = None):
        self.tehai = tehai
        self.tehaistr = tehaistr
        self.xiangtingshu = 8
        self.menzi = []
        if tehaistr != None:
            l = tehaistr.split('p')
            newTehai = []
            for item in l[0]:
                newTehai.append(Hai(item + 'p'))
            l2 = l[1].split('m')
            for item in l2[0]:
                newTehai.append(Hai(item + 'm'))
            l3 = l2[1].split('s')
            for item in l3[0]:
                newTehai.append(Hai(item + 's'))
            l4 = l3[1].split('z')
            for item in l4[0]:
                newTehai.append(Hai(item + 'z'))

            self.tehai = newTehai

    def check(self):
        self.haiList = []
        self.haiList.append([])
        self.haiList.append([])
        self.haiList.append([])
        self.haiList.append([])
        for i in self.tehai:
            if i.type == 'p':
                self.haiList[0].append(i)
            elif i.type == 'm':
                self.haiList[1].append(i)
            elif i.type == 's':
                self.haiList[2].append(i)
            elif i.type == 'z':
                self.haiList[3].append(i)

    def print(self):
        self.checkXiangTing(self.haiList[0])
        print('\n')
        self.checkXiangTing(self.haiList[1])
        print('\n')
        self.checkXiangTing(self.haiList[2])
        print('\n')
        self.checkXiangTing(self.haiList[3])
        print('\n')

        self.checkDazi(self.haiList[0])
        # self.checkDazi(self.haiList[1])
        # self.checkDazi(self.haiList[2])
        # self.checkDazi(self.haiList[3])

    def checkXiangTing(self, l: list):
        '''

        :param l:
        :return:
        '''
        for hai in l:
            if 'z' in hai.getName():
                break
            if '9' in hai.getName():
                continue
            nexthai = hai.next()
            if self.checkExist(nexthai, l):
                nexthai2 = nexthai.next()
                if self.checkExist(nexthai2, l):
                    hai.print()
                    nexthai.print()
                    nexthai2.print()
                    print('向听数减一')
                    self.xiangtingshu = self.xiangtingshu - 2
                    self.removeShunZi(hai, l)
                    self.checkXiangTing(l)
                    return None

        print(self.xiangtingshu)

        self.checkKeZi(l)

    def checkKeZi(self, l: list):

        for hai in l:
            count = sum(item.getName() == hai.getName() for item in l)
            if count == 3:
                print('向听数减一')
                self.xiangtingshu = self.xiangtingshu - 2
                self.removeKeZi(hai, l)
                self.checkKeZi(l)
                return None

        print(self.xiangtingshu)

    def removeKeZi(self, firsthai: Hai, l: list):
        count = 3
        for hai in l:
            if hai.getName() == firsthai.getName():
                l.remove(hai)
                count = count - 1

            if count == 0:
                break

        return None

    def checkDazi(self, l: list):
        for i in self.menzi:
            for j in l:
                if j.getName() == i.getName():
                    l.remove(j)

        print('lenth of hai is {}'.format(l.__len__()))
        if l.__len__() > 1:
            for i in range(0, l.__len__() - 1):
                if i < l.__len__() - 1:
                    dazi = Dazi(l[i], l[i + 1])
                    if dazi.isDazi():
                        l[i].print()
                        l[i + 1].print()
                        self.xiangtingshu = self.xiangtingshu - 1

        print(self.xiangtingshu)
        return None

    def removeShunZi(self, firsthai: Hai, hailist: list):
        secondhai = firsthai.next()
        thirdhai = secondhai.next()
        for hai in hailist:
            if hai.getName() == firsthai.getName():
                hailist.remove(hai)
                self.menzi.append(hai)
                break
        for hai in hailist:
            if hai.getName() == secondhai.getName():
                hailist.remove(hai)
                self.menzi.append(hai)
                break
        for hai in hailist:
            if hai.getName() == thirdhai.getName():
                hailist.remove(hai)
                self.menzi.append(hai)
                break

    def checkExist(self, hai: Hai, l: list):
        for item in l:
            if hai.getName() == item.getName():
                return True

        return False


if __name__ == "__main__":
    print('main start')
    tehai = TeHai(tehaistr='1229p47m147s1234z')
    tehai.check()
    tehai.print()
    # a = ['1', '1', '2', '2', '3']
    # b = ['1', '2', '3']
    # for i in a:
    #     for j in b:
    #         if i == j:
    #             a.remove(i)
    #             print('remove')
    #
    # print(a)
