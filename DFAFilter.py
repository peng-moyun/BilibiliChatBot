# -*- coding: utf-8 -*-
# @Author: zhangfujie
# @Date:   2019/10/22
# @Last Modified by:   zhangfujie
# @Last Modified time: 2019/10/22
# @ ---------- DFA过滤算 ---------- 
import time
time1 = time.time()

class DFAFilter(object):
	"""DFA过滤算法"""
	def __init__(self):
		super(DFAFilter, self).__init__()
		self.keyword_chains = {}
		self.delimit = '\x00'

	# 读取解析敏感词
	def parseSensitiveWords(self, path):
		ropen = open(path,'r')
		text = ropen.read()
		keyWordList = text.split(',')
		for keyword in keyWordList:
			self.addSensitiveWords(str(keyword).strip())

	# 生成敏感词树
	def addSensitiveWords(self, keyword):
		keyword = keyword.lower()
		chars = keyword.strip()
		if not chars:
			return
		level = self.keyword_chains
		for i in range(len(chars)):
			if chars[i] in level:
				level = level[chars[i]]
			else:
				if not isinstance(level, dict):
					break
				for j in range(i, len(chars)):
					level[chars[j]] = {}

					last_level, last_char = level, chars[j]

					level = level[chars[j]]
				last_level[last_char] = {self.delimit: 0}
				break
			if i == len(chars) - 1:
				level[self.delimit] = 0

	# 过滤敏感词
	def filterSensitiveWords(self, message, repl="*"):
		message = message.lower()
		ret = []
		start = 0
		while start < len(message):
			level = self.keyword_chains
			step_ins = 0
			message_chars = message[start:]
			for char in message_chars:
				if char in level:
					step_ins += 1
					if self.delimit not in level[char]:
						level = level[char]
					else:
						ret.append(repl * step_ins)
						start += step_ins - 1
						break
				else:
					ret.append(message[start])
					break
			start += 1

		return ''.join(ret)

	def Checksensitivewords(self, message, repl="*"):
		message = message.lower()
		ret = []
		start = 0
		while start < len(message):
			level = self.keyword_chains
			step_ins = 0
			message_chars = message[start:]
			for char in message_chars:
				if char in level:
					step_ins += 1
					if self.delimit not in level[char]:
						level = level[char]
					else:
						return True
				else:
					ret.append(message[start])
					break
			start += 1

		return False


if __name__ == "__main__":
	gfw = DFAFilter()
	gfw.parseSensitiveWords('min_word.txt')
	text = "「AI回复」不要这么没创意啊，提供点有趣的话题吧！来，给我个挑战，看我能不能把你逗乐！"
	result = gfw.filterSensitiveWords(text)
	print(result)
	text2 = "哦又是一个随便打招呼的人不要有事就快点说"
	result_Text = gfw.Checksensitivewords(text)
	print(result_Text)
	time2 = time.time()
	print('总共耗时:' + str(time2 - time1) + 's')