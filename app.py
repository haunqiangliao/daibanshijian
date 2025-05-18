import streamlit as st
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="待办事件管理器",
    page_icon="✅",
    layout="centered"
)

# 初始化 session_state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# 添加新任务
def add_task(task_content, priority):
    new_task = {
        "内容": task_content,
        "优先级": priority,
        "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "完成状态": False
    }
    st.session_state.tasks.append(new_task)

# 标记任务完成
def complete_task(index):
    st.session_state.tasks[index]["完成状态"] = True

# 删除任务
def delete_task(index):
    st.session_state.tasks.pop(index)

# 主界面
st.title("✅ 待办事件管理器 (演示版)")
st.write("使用 `st.session_state` 临时存储数据，刷新页面会重置。")

# 添加任务表单
with st.form("add_task_form"):
    task_content = st.text_input("任务内容", placeholder="输入任务...")
    priority = st.selectbox("优先级", ["低", "中", "高"], index=1)
    submitted = st.form_submit_button("添加任务")
    if submitted and task_content:
        add_task(task_content, priority)

# 显示任务列表
st.subheader("任务列表")

if not st.session_state.tasks:
    st.info("还没有任务，请添加一个吧！")
else:
    # 未完成任务
    st.markdown("### ⏳ 未完成")
    for i, task in enumerate(st.session_state.tasks):
        if not task["完成状态"]:
            col1, col2, col3 = st.columns([6, 2, 2])
            with col1:
                st.write(f"**{task['内容']}**")
                st.caption(f"创建于: {task['创建时间']} | 优先级: {task['优先级']}")
            with col2:
                if st.button("完成", key=f"complete_{i}"):
                    complete_task(i)
                    st.rerun()
            with col3:
                if st.button("删除", key=f"delete_{i}"):
                    delete_task(i)
                    st.rerun()
            st.divider()

    # 已完成任务
    st.markdown("### ✅ 已完成")
    has_completed = any(task["完成状态"] for task in st.session_state.tasks)
    if not has_completed:
        st.info("还没有完成的任务")
    else:
        for i, task in enumerate(st.session_state.tasks):
            if task["完成状态"]:
                st.write(f"~~{task['内容']}~~")
                st.caption(f"完成于: {task['创建时间']}")
                st.divider()
