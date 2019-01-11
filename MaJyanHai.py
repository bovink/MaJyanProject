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
                # min.next().print()
                pass

            if max.num - min.num == 1:
                if min.num == 1:
                    # max.next().print()
                    pass
                elif max == 9:
                    # min.previous().print()
                    pass
                else:
                    # min.previous().print()
                    # max.next().print()
                    pass

            if max.num - min.num == 0:
                # min.print()
                pass
        else:
            if max.num - min.num == 0:
                # min.print()
                pass


class CardList:

    def __init__(self, card_list: list, has_two_same_card=False, two_same_card: Hai = None):
        self.cardList = card_list
        self.completeCardsNum = 0
        self.inCompleteCardsNum = 0
        self.two_same_card = two_same_card
        self.baseNeedCard = 0
        self.baseMaxNeedCard = 0
        self.needCard = 0
        self.checkIfHasTwoSameCard(has_two_same_card)

    def checkIfHasTwoSameCard(self, has_two_same_card):
        if has_two_same_card:
            self.baseNeedCard = 3
            self.baseMaxNeedCard = 7
        else:
            self.baseNeedCard = 4
            self.baseMaxNeedCard = 8

    def calculate(self):
        if self.inCompleteCardsNum >= self.baseNeedCard - self.completeCardsNum:
            self.needCard = self.baseNeedCard - self.completeCardsNum
        else:
            self.needCard = self.baseMaxNeedCard - self.completeCardsNum * 2 - self.inCompleteCardsNum


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

    def check_head(self):
        self.cardCopy = []
        self.head = []
        for i in self.tehai:
            if sum(item.getName() == i.getName() for item in self.head) == 1:
                continue
            count = sum(card.getName() == i.getName() for card in self.tehai)
            if count >= 2:
                l = self.tehai[:]
                self.removeSameCard(i, l)
                self.cardCopy.append(l)
                self.head.append(i)

        print('contain head num is {}'.format(self.cardCopy.__len__()))

        if self.cardCopy.__len__() > 0:
            for i in self.cardCopy:
                self.xiangtingshu = 7
                self.check(i)
                self.print()
                print('#####')
        else:
            self.xiangtingshu = 8

    def check(self, l: list):
        self.haiList = []
        self.haiList.append([])
        self.haiList.append([])
        self.haiList.append([])
        self.haiList.append([])
        for i in l:
            if i.type == 'p':
                self.haiList[0].append(i)
            elif i.type == 'm':
                self.haiList[1].append(i)
            elif i.type == 's':
                self.haiList[2].append(i)
            elif i.type == 'z':
                self.haiList[3].append(i)

    def print(self):
        self.checkKeZi(self.haiList[0])
        self.checkKeZi(self.haiList[1])
        self.checkKeZi(self.haiList[2])
        self.checkKeZi(self.haiList[3])

        self.checkDazi(self.haiList[0])
        self.checkDazi(self.haiList[1])
        self.checkDazi(self.haiList[2])
        self.checkDazi(self.haiList[3])

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
                    # hai.print()
                    # nexthai.print()
                    # nexthai2.print()
                    print('顺子')
                    self.xiangtingshu = self.xiangtingshu - 2
                    self.removeShunZi(hai, l)
                    self.checkXiangTing(l)
                    return None

        # print(self.xiangtingshu)

        # self.checkKeZi(l)

    def checkKeZi(self, l: list):

        for hai in l:
            count = sum(item.getName() == hai.getName() for item in l)
            if count >= 3:
                print('刻子')
                self.xiangtingshu = self.xiangtingshu - 2
                self.removeSameCard(hai, l, count=3)
                self.checkKeZi(l)
                return None

        # print(self.xiangtingshu)
        self.checkXiangTing(l)

    def removeSameCard(self, card: Hai, list: list, count=2):
        for hai in list:
            if hai.getName() == card.getName():
                list.remove(hai)
                count = count - 1
                if count == 0:
                    break
                self.removeSameCard(card, list, count=count)
                break

        return None

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

        # print('lenth of hai is {}'.format(l.__len__()))
        if l.__len__() > 1:
            for i in range(0, l.__len__() - 1):
                if i < l.__len__() - 1:
                    dazi = Dazi(l[i], l[i + 1])
                    if dazi.isDazi():
                        # l[i].print()
                        # l[i + 1].print()
                        self.xiangtingshu = self.xiangtingshu - 1

        # print(self.xiangtingshu)
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
    tehai = TeHai(tehaistr='111222333p11m23s')
    tehai.check_head()
    # tehai.check()
    # tehai.print()
    # a = ['1', '1', '2', '2', '3']
    # b = ['1', '2', '3']
    # for i in a:
    #     for j in b:
    #         if i == j:
    #             a.remove(i)
    #             print('remove')
    #
    # print(a)
