import json
import os
import datetime

class TodoManager:
    def __init__(self, filename="todos.json"):
        self.filename = filename
        self.todos = self.load_todos()
        
    def load_todos(self):
        """从文件加载待办事项"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_todos(self):
        """保存待办事项到文件"""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.todos, file, ensure_ascii=False, indent=2)
    
    def add_todo(self, task, due_date=None):
        """添加新的待办事项"""
        new_todo = {
            "id": len(self.todos) + 1,
            "task": task,
            "completed": False,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "due_date": due_date
        }
        self.todos.append(new_todo)
        self.save_todos()
        return new_todo
    
    def list_todos(self):
        """列出所有待办事项"""
        if not self.todos:
            return "没有待办事项！"
        
        result = []
        for todo in self.todos:
            status = "[✓]" if todo["completed"] else "[ ]"
            due_info = f" | 截止日期: {todo['due_date']}" if todo["due_date"] else ""
            result.append(f"{todo['id']}. {status} {todo['task']}{due_info}")
        
        return "\n".join(result)
    
    def mark_complete(self, todo_id):
        """标记待办事项为已完成"""
        for todo in self.todos:
            if todo["id"] == todo_id:
                todo["completed"] = True
                self.save_todos()
                return True
        return False
    
    def delete_todo(self, todo_id):
        """删除待办事项"""
        original_length = len(self.todos)
        self.todos = [todo for todo in self.todos if todo["id"] != todo_id]
        
        # 重新编号
        for i, todo in enumerate(self.todos, 1):
            todo["id"] = i
        
        if len(self.todos) < original_length:
            self.save_todos()
            return True
        return False
    
    def get_stats(self):
        """获取待办事项统计信息"""
        total = len(self.todos)
        completed = sum(1 for todo in self.todos if todo["completed"])
        pending = total - completed
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }

def main():
    manager = TodoManager()
    
    while True:
        print("\n" + "=" * 30)
        print("      待办事项管理器")
        print("=" * 30)
        print("1. 添加待办事项")
        print("2. 查看所有待办事项")
        print("3. 标记待办事项为已完成")
        print("4. 删除待办事项")
        print("5. 查看统计信息")
        print("q. 退出")
        print("=" * 30)
        
        choice = input("请选择操作: ").lower()
        
        if choice == "1":
            task = input("输入待办事项: ").strip()
            if not task:
                print("待办事项不能为空！")
                continue
                
            due_date = input("输入截止日期 (YYYY-MM-DD, 可选): ").strip() or None
            if due_date and len(due_date) != 10:
                print("日期格式不正确，应为YYYY-MM-DD")
                due_date = None
                
            new_todo = manager.add_todo(task, due_date)
            print(f"已添加: {new_todo['task']}")
            
        elif choice == "2":
            print("\n待办事项列表:")
            print(manager.list_todos())
            
        elif choice == "3":
            try:
                todo_id = int(input("输入要标记为已完成的待办事项ID: "))
                if manager.mark_complete(todo_id):
                    print(f"待办事项 #{todo_id} 已标记为已完成")
                else:
                    print(f"未找到待办事项 #{todo_id}")
            except ValueError:
                print("请输入有效的数字ID")
                
        elif choice == "4":
            try:
                todo_id = int(input("输入要删除的待办事项ID: "))
                if manager.delete_todo(todo_id):
                    print(f"待办事项 #{todo_id} 已删除")
                else:
                    print(f"未找到待办事项 #{todo_id}")
            except ValueError:
                print("请输入有效的数字ID")
                
        elif choice == "5":
            stats = manager.get_stats()
            print(f"\n待办事项统计:")
            print(f"总数: {stats['total']}")
            print(f"已完成: {stats['completed']}")
            print(f"未完成: {stats['pending']}")
            
        elif choice == "q":
            print("感谢使用待办事项管理器，再见！")
            break
            
        else:
            print("无效选择，请重试")

if __name__ == "__main__":
    main()
