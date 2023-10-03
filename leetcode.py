# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def removeDuplicateLetters(self, s: str) -> str:
        """
        Given a string s, remove duplicate letters so that every letter appears once and only once. You must make sure your result is
         the smallest in lexicographical order among all possible results.
        :param s: 1 <= s.length <= 10^4
        :return:
        """
        alphabet = set(s)
        s_len = len(s)
        last_occ = {i: s_len - 1 - s[::-1].index(i) for i in alphabet}
        visited = set(s[0])
        stack = [s[0]]
        for i in range(len(s)):
            if s[i] not in visited:
                while s[i] < stack[-1] and i < last_occ[stack[-1]]:
                    visited.remove(stack[-1])
                    stack.pop()
                    if (stack or [None])[-1] is None:
                        break
                if i <= last_occ[s[i]]:
                    stack.append(s[i])
                    visited.add(s[i])
        return ''.join(stack)

    def decodeAtIndex(self, s: str, k: int) -> str:
        """
        You are given an encoded string s. To decode the string to a tape,
         the encoded string is read one character at a time and the following steps are taken:
        If the character read is a letter, that letter is written onto the tape.
        If the character read is a digit d, the entire current tape is repeatedly written d - 1 more times in total.
        :param s: 2 <= s.length <= 100
        :param k: 1 <= k <= 10^9
        :return: Given an integer k, return the k^th letter (1-indexed) in the decoded string.
        """
        length = 0
        i = 0
        while length < k:
            char = ord(s[i])
            if 50 <= char < 58:
                length *= (char - 48)
            else:
                length += 1
            i += 1

        for j in range(i - 1, -1, -1):
            char = s[j]
            print(char)
            if '1' < char <= '9':
                length //= (ord(char) - 48)
                k %= length
            else:
                if k == 0 or k == length:
                    return char
                length -= 1

    def haveConflict(self, event1: list[str], event2: list[str]) -> bool:
        """
        You are given two arrays of strings that represent two inclusive events that happened on the same day,
         event1 and event2, where:
         Event times are valid 24 hours format in the form of HH:MM.
        A conflict happens when two events have some non-empty intersection (i.e., some moment is common to both events).

        Return true if there is a conflict between two events. Otherwise, return false.
        :param event1: ['HH:MM','HH:MM']
        :param event2: ['HH:MM','HH:MM']
        :return: True or False
        """
        # event1 = [event1[0].split(':'), event1[1].split(':')]
        # event2 = [event2[0].split(':'), event2[1].split(':')]
        # event1[0], event1[1] = int(event1[0][0]) * 60 + int(event1[0][1]), int(event1[1][0]) * 60 + int(event1[1][1])
        # event2[0], event2[1] = int(event2[0][0]) * 60 + int(event2[0][1]), int(event2[1][0]) * 60 + int(event2[1][1])
        return (event2[0] <= event1[0] <= event2[1]) \
            or (event2[0] <= event1[1] <= event2[1]) \
            or (event1[1] > event2[0] > event1[0])

    def isMonotonic(self, nums: list[int]) -> bool:
        """
        An array is monotonic if it is either monotone increasing or monotone decreasing.
        Given an integer array nums, return true if the given array is monotonic, or false otherwise.
        :param nums: int List
        :return: Bool
        """
        j = nums[0]
        for i in nums[1:]:
            if (j > i and j > nums[0]) or (j < i and j < nums[0]):
                return False
            j = i
        return True

    def winnerOfGame(self, colors: str) -> bool:
        """
        There are n pieces arranged in a line, and each piece is colored either by 'A' or by 'B'.
        You are given a string colors of length n where colors[i] is the color of the ith piece.
        Alice and Bob are playing a game where they take alternating turns removing pieces from the line.
        In this game, Alice moves first.
         Alice is only allowed to remove a piece colored 'A' if both its neighbors are also colored 'A'. She is not allowed to remove pieces that are colored 'B'.
         Bob is only allowed to remove a piece colored 'B' if both its neighbors are also colored 'B'. He is not allowed to remove pieces that are colored 'A'.
         Alice and Bob cannot remove pieces from the edge of the line.
         If a player cannot make a move on their turn, that player loses and the other player wins.
        Assuming Alice and Bob play optimally, return true if Alice wins, or return false if Bob wins.
        :param colors: string of 'A' and 'B'
        :return: bool True if Alice wins
        """
        dict_win = {'A': 0, 'B': 0}
        for i in range(1, len(colors) - 1):
            if colors[i] == colors[i - 1] == colors[i + 1]:
                dict_win[colors[i]] += 1
        return dict_win['A'] > dict_win['B']

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        """
        You are given two non-empty linked lists representing two non-negative integers.
         The digits are stored in reverse order, and each of their nodes contains a single digit.
          Add the two numbers and return the sum as a linked list.
        You may assume the two numbers do not contain any leading zero, except the number 0 itself.
        :param l1: first node of linked right list
        :param l2: first node of linked right list
        :return:
        """
        zero_node = ListNode()
        l_result = ListNode(val=l1.val + l2.val)
        first_node = l_result
        while l1.next or l2.next:
            l1 = l1.next if l1.next is not None else zero_node
            l2 = l2.next if l2.next is not None else zero_node
            if l_result.val < 10:
                val = 0
            else:
                val = 1
                l_result.val -= 10
            l_result.next = ListNode(l1.val + l2.val + val)
            l_result = l_result.next
        if l_result.val >= 10:
            l_result.val -= 10
            l_result.next = ListNode(val=1)
        return first_node

    def numIdenticalPairs(self, nums: list[int]) -> int:
        """
        Given an array of integers nums, return the number of good pairs.
        A pair (i, j) is called good if nums[i] == nums[j] and i < j.
        [1,2,3,1,1,3] -> 4; [1,1,1,1] -> 6
        :param nums:
        :return:
        """
        result = 0
        dict_nums = {}
        for i in nums:
            if i in dict_nums:
                dict_nums[i] += 1
                result += dict_nums[i]
            else:
                dict_nums[i] = 0
        return result
