# Definition for singly-linked list.
from functools import cache
from typing import Optional
import collections


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

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

    def integerBreak(self, n: int) -> int:
        """
        Given an integer n, break it into the sum of k positive integers, where k >= 2,
         and maximize the product of those integers.
        :param n: 2 <= n <= 58
        :return: int
        """
        if n == 2 or n == 3:
            return n - 1
        result = 1
        while n > 4:
            n -= 3
            result *= 3
        return result * n

    def majorityElement(self, nums: list[int]) -> list[int]:
        """
        Given an integer array of size n, find all elements that appear more than ⌊ n/3 ⌋ times.
        :param nums: 1 <= nums.length <= 5 * 10**4; -10**9 <= nums[i] <= 10**9
        :return:
        """
        n = len(nums)
        result = set()
        dict_of_nums = {x: 0 for x in set(nums)}
        for i in nums:
            dict_of_nums[i] += 1
            if dict_of_nums[i] > n / 3:
                result.add(i)
        return list(result)


    def amountOfTime(self, root: Optional[TreeNode], start: int) -> int:
        """
        You are given the root of a binary tree with unique values, and an integer start.
        At minute 0, an infection starts from the node with value start.
        Each minute, a node becomes infected if:
            The node is currently uninfected.
            The node is adjacent to an infected node.
            Return the number of minutes needed for the entire tree to be infected.
        :param self:
        :param root:
        :param start:
        :return:
        """
        self.nodes_stack = [[start,0,-1]]
        self.roads_data = collections.defaultdict(lambda: [])
        result = 0
        def makeGraf(tree_root: TreeNode):
            if tree_root.left:
                self.roads_data[tree_root.val] += [tree_root.left.val]
                self.roads_data[tree_root.left.val] += [tree_root.val]
                makeGraf(tree_root.left)
            if tree_root.right:
                self.roads_data[tree_root.val] += [tree_root.right.val]
                self.roads_data[tree_root.right.val] += [tree_root.val]
                makeGraf(tree_root.right)
            return 0
        def findRoads(node):
            # [node.val, time to find, prew_node]
            for i in self.roads_data[node[0]]:
                if i != node[2]:
                    self.nodes_stack.append([i,node[1] + 1,node[0]])
        makeGraf(root)
        while len(self.nodes_stack) != 0:
            iter_node = self.nodes_stack.pop()
            findRoads(iter_node)
            if iter_node[1] > result:
                result = iter_node[1]
        return result


    mod = (10**9+7)
    def numRollsToTarget(self, n: int, k: int, target: int) -> int:
        """
        You have n dice, and each dice has k faces numbered from 1 to k.
        Given three integers n, k, and target, return the number of possible ways
        (out of the kn total ways) to roll the dice, so the sum of the face-up numbers equals
        target. Since the answer may be too large,
        return it modulo 109 + 7.
        :param n:
        :param k:
        :param target:
        :return:
        """
        @cache
        def counter(target:int, n: int):
            res = 0
            if n == 0 and target != 0:
                return 0
            if target > 0 and n > 0:
                for i in range(1,k+1):
                    res += counter(target - i,n - 1)
            elif target == 0 and n == 0:
                return 1
            else:
                return 0
            return res

        return counter(target,n) % self.mod

    def numDecodings(self, s: str) -> int:
        """
        A message containing letters from A-Z can be encoded into numbers using the following mapping:

        'A' -> "1"
        'B' -> "2"
        ...
        'Z' -> "26"
        To decode an encoded message, all the digits must be grouped then mapped back
         into letters using the reverse of the mapping above (there may be multiple ways).
          For example, "11106" can be mapped into:
            "AAJF" with the grouping (1 1 10 6)
            "KJF" with the grouping (11 10 6)
        Note that the grouping (1 11 06) is invalid because "06" cannot be mapped into 'F' since "6" is different from "06".
        Given a string s containing only digits, return the number of ways to decode it.
        The test cases are generated so that the answer fits in a 32-bit integer.
        :param s:
        :return:
        """
        curr, oneback, twoback = 0, 1, 1
        for i in range(len(s) - 1, -1, -1):
            if s[i] == '0':
                curr = 0
            else:
                curr = oneback
                if i + 1 < len(s) and int(s[i] + s[i + 1]) <= 26:
                    curr += twoback
            twoback = oneback
            oneback = curr
        return curr