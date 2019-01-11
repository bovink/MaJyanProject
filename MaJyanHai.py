# 牌的类别为筒，万，索，字牌
# 筒，万，索的数字就从1到9，字牌的顺序为东南西北白发中
import math


class Card:

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
        return Card(l)

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
        return Card(l)

    def print(self):
        print('hai is {}{}'.format(self.num, self.type))


class IncompleteCard:

    def __init__(self, card1: Card, card2: Card):
        self.card1 = card1
        self.card2 = card2

    def isDazi(self):
        if self.card1.num < self.card2.num:
            min = self.card1
            max = self.card2
        else:
            min = self.card2
            max = self.card1

        if self.card1.type in ['p', 'm', 's']:
            if max.num - min.num < 3:
                return True
        else:
            if max.num - min.num == 0:
                return True

        return False

    def need(self):
        if self.card1.num < self.card2.num:
            min = self.card1
            max = self.card2
        else:
            min = self.card2
            max = self.card1

        if self.card1.type in ['p', 'm', 's']:
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

    def __init__(self, cardList: list, hasTwoSameCard=False, twoSameCard: Card = None):
        self.cardList = cardList
        self.completeCardsNum = 0
        self.incompleteCardsNum = 0
        self.two_same_card = twoSameCard
        self.baseNeedCard = 0
        self.baseMaxNeedCard = 0
        self.needCard = 0
        self.checkIfHasTwoSameCard(hasTwoSameCard)

    def checkIfHasTwoSameCard(self, hasTwoSameCard):
        if hasTwoSameCard:
            self.baseNeedCard = 4
            self.baseMaxNeedCard = 8
        else:
            self.baseNeedCard = 5
            self.baseMaxNeedCard = 9

    def calculate(self):
        if self.incompleteCardsNum >= self.baseNeedCard - self.completeCardsNum:
            self.needCard = self.baseNeedCard - self.completeCardsNum
        else:
            self.needCard = self.baseMaxNeedCard - self.completeCardsNum * 2 - self.incompleteCardsNum

    def print(self):
        print('面子数:{}，搭子数:{}'.format(self.completeCardsNum, self.incompleteCardsNum))
        print('现在缺{}张胡牌'.format(self.needCard))

    def addCompleteCardsNum(self):
        self.completeCardsNum += 1

    def addInCompleteCardNum(self):
        self.incompleteCardsNum += 1

    def getCardList(self):
        return self.cardList

    def getNeedCard(self):
        return self.needCard


# 4个面子1个雀头 面子可为顺子或者刻子
# 如果所有牌都不搭，按一般形来做牌的话，即一张浮牌需要摸进2次有效自摸才能形成面子，那4个面子即需要8次有效自摸即可形成单吊听牌

class Analyser:

    def __init__(self, tehai: list = None, tehaistr: str = None):
        self.tehai = tehai
        self.tehaistr = tehaistr
        self.xiangtingshu = 8
        self.menzi = []
        if tehaistr != None:
            l = tehaistr.split('p')
            newTehai = []
            for item in l[0]:
                newTehai.append(Card(item + 'p'))
            l2 = l[1].split('m')
            for item in l2[0]:
                newTehai.append(Card(item + 'm'))
            l3 = l2[1].split('s')
            for item in l3[0]:
                newTehai.append(Card(item + 's'))
            l4 = l3[1].split('z')
            for item in l4[0]:
                newTehai.append(Card(item + 'z'))

            self.tehai = newTehai

    def check_head(self, needCheckHead=True):
        self.cardCopy = []
        self.head = []
        for i in self.tehai:
            if sum(item.getName() == i.getName() for item in self.head) == 1:
                continue
            count = sum(card.getName() == i.getName() for card in self.tehai)
            if needCheckHead:
                head = 2
            else:
                head = 1
            if count >= head:
                # 有雀头
                l = self.tehai[:]
                self.removeSameCard(i, l, count=head)
                if needCheckHead:
                    cardList = CardList(l, hasTwoSameCard=True, twoSameCard=i)
                else:
                    cardList = CardList(l, hasTwoSameCard=False, twoSameCard=i)

                self.cardCopy.append(cardList)
                self.head.append(i)

        print('contain head num is {}'.format(self.cardCopy.__len__()))

        needCard = 9
        needLeastCards = []
        if self.cardCopy.__len__() > 0:
            for i in self.cardCopy:
                self.xiangtingshu = 7
                self.menzi = []
                self.check(i)
                self.print(i)
                i.calculate()
                if i.getNeedCard() < needCard:
                    needCard = i.getNeedCard()
                    needLeastCards = []
                    needLeastCards.append(i)
                elif i.getNeedCard() == needCard:
                    needLeastCards.append(i)

        for m in needLeastCards:
            m.print()

    def check(self, cardList: CardList):
        self.haiList = []
        self.haiList.append([])
        self.haiList.append([])
        self.haiList.append([])
        self.haiList.append([])
        for i in cardList.getCardList():
            if i.type == 'p':
                self.haiList[0].append(i)
            elif i.type == 'm':
                self.haiList[1].append(i)
            elif i.type == 's':
                self.haiList[2].append(i)
            elif i.type == 'z':
                self.haiList[3].append(i)

    def print(self, cardList: CardList):
        self.checkKeZi(self.haiList[0], cardList)
        self.checkKeZi(self.haiList[1], cardList)
        self.checkKeZi(self.haiList[2], cardList)
        self.checkKeZi(self.haiList[3], cardList)

        self.checkDazi(self.haiList[0], self.menzi, cardList)
        self.checkDazi(self.haiList[1], self.menzi, cardList)
        self.checkDazi(self.haiList[2], self.menzi, cardList)
        self.checkDazi(self.haiList[3], self.menzi, cardList)

    def checkXiangTing(self, l: list, cardList: CardList):
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
                    self.xiangtingshu = self.xiangtingshu - 2
                    self.removeShunZi(hai, l)
                    cardList.addCompleteCardsNum()
                    self.checkXiangTing(l, cardList)
                    return None

        # print(self.xiangtingshu)

        # self.checkKeZi(l)

    def checkKeZi(self, l: list, cardList: CardList):

        for hai in l:
            count = sum(item.getName() == hai.getName() for item in l)
            if count >= 3:
                self.xiangtingshu = self.xiangtingshu - 2
                self.removeSameCard(hai, l, count=3)
                cardList.addCompleteCardsNum()
                self.checkKeZi(l, cardList)
                return None

        # print(self.xiangtingshu)
        self.checkXiangTing(l, cardList)

    def removeSameCard(self, card: Card, list: list, count=2):
        for hai in list:
            if hai.getName() == card.getName():
                list.remove(hai)
                self.menzi.append(hai)
                count = count - 1
                if count == 0:
                    break
                self.removeSameCard(card, list, count=count)
                break

        return None

    def removeKeZi(self, firsthai: Card, l: list):
        count = 3
        for hai in l:
            if hai.getName() == firsthai.getName():
                l.remove(hai)
                count = count - 1

            if count == 0:
                break

        return None

    def checkDazi(self, l: list, removeList: list, cardList: CardList):
        for i in removeList:
            for j in l:
                if j.getName() == i.getName():
                    l.remove(j)

        # print('lenth of hai is {}'.format(l.__len__()))
        if l.__len__() > 1:
            for i in range(0, l.__len__() - 1):
                if i < l.__len__() - 1:
                    dazi = IncompleteCard(l[i], l[i + 1])
                    if dazi.isDazi():
                        # l[i].print()
                        # l[i + 1].print()
                        cardList.addInCompleteCardNum()
                        self.xiangtingshu = self.xiangtingshu - 1
                        newRemoveList = [l[i], l[i + 1]]
                        self.checkDazi(l, newRemoveList, cardList)
                        return None

        # print(self.xiangtingshu)
        return None

    def removeShunZi(self, firsthai: Card, hailist: list):
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

    def checkExist(self, hai: Card, l: list):
        for item in l:
            if hai.getName() == item.getName():
                return True

        return False


if __name__ == "__main__":
    print('main start')
    tehai = Analyser(tehaistr='3444567p123m111s')
    tehai.check_head()
    tehai.check_head(needCheckHead=False)
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
