import math
from data_structures import Node, search_from_head

def linked_string(string: str, index=0, last_node=None, link_head=None):
    node = Node(string[index])
    if last_node is not None:
        node.left = last_node
        last_node.right = node
    else:
        link_head = node
    index += 1
    last_node = node
    return link_head, linked_string(string, index, last_node, link_head) if index < len(string) else node

def combine_values(linked_string_start):
    node = linked_string_start
    while True:
        if node.reference.isdigit() or node.reference == '.':
            start_node = node
            full_value = node.reference
            node = node.right
            while True:
                if node is None:
                    end_node = start_node
                    break
                if node.reference.isdigit() or node.reference == '.':
                    full_value += node.reference
                    if node.right is not None:
                        node = node.right
                    else:
                        end_node = node
                        break
                else:
                    end_node = node.left
                    break
            new_node = Node(full_value)
            left = start_node.left
            right = end_node.right
            if left is not None:
                left.right = new_node
                new_node.left = left
            else:
                linked_string_start = new_node
            if right is not None:
                right.left = new_node
                new_node.right = right
            else:
                break
            node = new_node
        node = node.right
        if node is None:
            break
    return linked_string_start

def replace_node(old_node: Node, new_node: Node, overall_head):
    val1 = old_node.left
    val2 = old_node.right
    left = val1.left
    right = val2.right
    if left is not None:
        left.right = new_node
        new_node.left = left
    else:
        overall_head = new_node
    if right is not None:
        right.left = new_node
        new_node.right = right
    return overall_head

def replace_all(overall_head, char: str, operation):
    node = search_from_head(overall_head, char)
    if node is None:
        return overall_head
    val1 = node.left
    val2 = node.right
    operated = operation(float(val1.reference), float(val2.reference))
    result = Node(str(operated))
    overall_head = replace_node(node, result, overall_head)

    return replace_all(overall_head, char, operation)
# PEMDAS
def __solve(head_of_expression:Node, parenthesized = False):
    overall_head = head_of_expression
    if not parenthesized: # Check for Parenthesis
        node = overall_head
        closes = 0
        while True:
            if node.reference == '(':
                opening = node
                node = node.right
                while True:
                    if node.reference == '(':
                        closes += 1
                    if node.reference == ')':
                        if closes == 0:
                            has_closing = True
                            break
                        else:
                            closes -= 1
                    if node.right is None:
                        has_closing = False
                        break
                    node = node.right
                closing = node
                left = opening.left
                right = closing.right

                # Detach parenthesis
                opening.right.left = None
                closing.left.right = None if has_closing else closing

                result = __solve(opening.right)

                if left is not None:
                    if left.reference != '+' and left.reference != '-' and left.reference != '*' and left.reference != '/' and left.reference != '^' and left.reference != '(':
                        auto_mult = Node('*')
                        auto_mult.left = left
                        left.right = auto_mult
                        left = auto_mult
                    left.right = result
                    result.left = left
                else:
                    overall_head = result
                if right is not None:
                    if right.reference != '+' and right.reference != '-' and right.reference != '*' and right.reference != '/' and right.reference != '^' and right.reference != ')':
                        auto_mult = Node('*')
                        right.left = auto_mult
                        auto_mult.right = right
                        right = auto_mult
                    right.left = result
                    result.right = right
                # debug(overall_head)
                return __solve(overall_head, parenthesized=False)
            if node.reference == ')':
                opening = overall_head
                closing = node
                right = closing.right

                # Detach parenthesis
                closing.left.right = None

                result = __solve(opening)
                overall_head = result

                if right is not None:
                    right.left = result
                    result.right = right
                return __solve(overall_head, parenthesized=False)
            node = node.right
            if node is None:
                break
        return __solve(overall_head, parenthesized=True)
    else:
        overall_head = replace_all(overall_head, "^", lambda x,y: x**y)
        overall_head = replace_all(overall_head, "*", lambda x,y: x*y)
        overall_head = replace_all(overall_head, "/", lambda x,y: x/y)
        overall_head = replace_all(overall_head, "+", lambda x,y: x+y)
        overall_head = replace_all(overall_head, "-", lambda x,y: x-y)
        return overall_head

def solve_equation(equation_string: str):
    try:
        head, tail = linked_string(equation_string.replace(' ', ''))
        head = combine_values(head)
        return float(__solve(head).reference)
    except:
        return None

solve_equation("1+1")