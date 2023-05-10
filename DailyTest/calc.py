import re


class Calculator:
	def calculate(self, expression):
		# 定义正则表达式
		pattern = r'(\d+|\+|\-|\*|\/|\(|\))'

		# 对表达式进行分词
		tokens = re.findall(pattern, expression)

		# 将中缀表达式转化为后缀表达式
		postfix = self.infix_to_postfix(tokens)

		# 计算后缀表达式的值
		result = self.evaluate_postfix(postfix)

		return result

	def infix_to_postfix(self, tokens):
		# 定义运算符优先级
		precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

		# 初始化空栈和空后缀表达式
		stack = []
		postfix = []

		# 遍历中缀表达式的每个元素
		for token in tokens:
			if token.isdigit():
				# 如果当前元素是数字，直接将其加入后缀表达式
				postfix.append(token)
			elif token in '+-*/':
				# 如果当前元素是运算符，先将栈中优先级高于或等于它的运算符弹出并加入后缀表达式，
				# 然后将当前运算符入栈
				while stack and stack[-1] in '+-*/' and precedence[token] <= precedence[stack[-1]]:
					postfix.append(stack.pop())
				stack.append(token)
			elif token == '(':
				# 如果当前元素是左括号，直接入栈
				stack.append(token)
			elif token == ')':
				# 如果当前元素是右括号，将栈中左括号上面的元素全部弹出并加入后缀表达式，
				# 然后将左括号出栈
				while stack and stack[-1] != '(':
					postfix.append(stack.pop())
				stack.pop()

		# 将栈中剩余的元素全部弹出并加入后缀表达式
		while stack:
			postfix.append(stack.pop())

		return postfix

	def evaluate_postfix(self, postfix):
		# 初始化空栈
		stack = []

		# 遍历后缀表达式的每个元素
		for token in postfix:
			if token.isdigit():
				# 如果当前元素是数字，直接入栈
				stack.append(int(token))
			elif token in '+-*/':
				# 如果当前元素是运算符，从栈中弹出两个元素进行运算，再将结果入栈
				b = stack.pop()
				a = stack.pop()
				if token == '+':
					stack.append(a + b)
				elif token == '-':
					stack.append(a - b)
				elif token == '*':
					stack.append(a * b)
				elif token == '/':
					stack.append(a / b)

		return stack.pop()


# 测试代码
calculator = Calculator()
expression = '1 + 2 * (3 - 4) / 5'
result = calculator.calculate(expression)
print(f'{expression} = {result}')
