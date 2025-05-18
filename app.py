import streamlit as st
from datetime import datetime, timedelta

# 页面配置
st.set_page_config(
    page_title="待办事件管理器 (含截止日期)",
    page_icon="⏰",
    layout="centered"
)

# 初始化 session_state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# 添加新任务
def add_task(task_content, priority, due_date):
    new_task = {
        "内容": task_content,
        "优先级": priority,
        "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "截止日期": due_date.strftime("%Y-%m-%d %H:%M") if due_date else "无",
        "完成状态": False
    }
    st.session_state.tasks.append(new_task)

# 标记任务完成
def complete_task(index):
    st.session_state.tasks[index]["完成状态"] = True

# 删除任务
def delete_task(index):
    st.session_state.tasks.pop(index)

# 检查任务是否临近截止
def check_due_soon(due_date_str):
    if due_date_str == "无":
        return False
    due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
    return due_date - datetime.now() < timedelta(hours=24)

# 主界面
st.title("⏰ 待办事件管理器 (含截止日期)")
st.write("使用 `st.session_state` 临时存储数据，刷新页面会重置。")

# 添加任务表单
with st.form("add_task_form"):
    task_content = st.text_input("任务内容", placeholder="输入任务...")
    col1, col2 = st.columns(2)
    with col1:
        priority = st.selectbox("优先级", ["低", "中", "高"], index=1)
    with col2:
        due_date = st.date_input("截止日期", min_value=datetime.today())
        due_time = st.time_input("截止时间", value=datetime.now().time())
        full_due_date = datetime.combine(due_date, due_time)
    
    submitted = st.form_submit_button("添加任务")
    if submitted and task_content:
        add_task(task_content, priority, full_due_date)

# 显示任务列表
st.subheader("我的任务")

if not st.session_state.tasks:
    st.info("还没有任务，请添加一个吧！")
else:
    # 未完成任务（按截止日期排序）
    st.markdown("### ⏳ 未完成")
    incomplete_tasks = [task for task in st.session_state.tasks if not task["完成状态"]]
    incomplete_tasks.sort(key=lambda x: x["截止日期"] if x["截止日期"] != "无" else "9999-12-31")
    
    for i, task in enumerate(incomplete_tasks):
        original_index = st.session_state.tasks.index(task)  # 获取原始索引
        col1, col2, col3 = st.columns([6, 2, 2])
        with col1:
            # 如果任务临近截止，显示红色警告
            if check_due_soon(task["截止日期"]):
                st.error(f"⚠️ **{task['内容']}** (截止: {task['截止日期']})")
            else:
                st.write(f"**{task['内容']}**")
            st.caption(f"优先级: {task['优先级']} | 创建于: {task['创建时间']}")
        with col2:
            if st.button("完成", key=f"complete_{original_index}"):
                complete_task(original_index)
                st.rerun()
        with col3:
            if st.button("删除", key=f"delete_{original_index}"):
                delete_task(original_index)
                st.rerun()
        st.divider()

    # 已完成任务
    st.markdown("### ✅ 已完成")
    completed_tasks = [task for task in st.session_state.tasks if task["完成状态"]]
    if not completed_tasks:
        st.info("还没有完成的任务")
    else:
        for i, task in enumerate(completed_tasks):
            st.write(f"~~{task['内容']}~~")
            st.caption(f"完成于: {task['创建时间']} | 原截止: {task['截止日期']}")
            st.divider()
