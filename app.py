import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 页面配置
st.set_page_config(
    page_title="待办事件管理器",
    page_icon="✅",
    layout="centered"
)

# 数据文件路径
DATA_FILE = "todo_data.csv"

# 初始化数据
def init_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["任务内容", "优先级", "创建时间", "完成状态"])
        df.to_csv(DATA_FILE, index=False)
    else:
        df = pd.read_csv(DATA_FILE)
    return df

# 保存数据
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# 主应用
def main():
    st.title("✅ 待办事件管理器")
    st.write("一个简单易用的待办事项管理工具")
    
    # 初始化或加载数据
    df = init_data()
    
    # 侧边栏 - 添加新任务
    with st.sidebar:
        st.subheader("添加新任务")
        new_task = st.text_input("任务内容", placeholder="输入任务内容...")
        priority = st.selectbox("优先级", ["低", "中", "高"], index=1)
        if st.button("添加任务"):
            if new_task:
                new_row = {
                    "任务内容": new_task,
                    "优先级": priority,
                    "创建时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "完成状态": False
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_data(df)
                st.success("任务已添加!")
            else:
                st.warning("请输入任务内容")
    
    # 主界面 - 显示任务列表
    st.subheader("我的待办事项")
    
    # 显示未完成任务
    st.markdown("### 未完成的任务")
    incomplete_tasks = df[df["完成状态"] == False]
    
    if incomplete_tasks.empty:
        st.info("🎉 没有未完成的任务!")
    else:
        for idx, row in incomplete_tasks.iterrows():
            col1, col2, col3, col4 = st.columns([5, 2, 1, 1])
            with col1:
                st.write(f"📌 {row['任务内容']}")
            with col2:
                st.write(f"优先级: {row['优先级']}")
            with col3:
                if st.button("完成", key=f"complete_{idx}"):
                    df.at[idx, "完成状态"] = True
                    save_data(df)
                    st.experimental_rerun()
            with col4:
                if st.button("删除", key=f"delete_{idx}"):
                    df = df.drop(index=idx).reset_index(drop=True)
                    save_data(df)
                    st.experimental_rerun()
            st.divider()
    
    # 显示已完成任务
    st.markdown("### 已完成的任务")
    completed_tasks = df[df["完成状态"] == True]
    
    if completed_tasks.empty:
        st.info("还没有完成的任务")
    else:
        for idx, row in completed_tasks.iterrows():
            col1, col2, col3 = st.columns([5, 2, 1])
            with col1:
                st.write(f"✅ ~~{row['任务内容']}~~")
            with col2:
                st.write(f"完成于: {row['创建时间']}")
            with col3:
                if st.button("删除", key=f"delete_completed_{idx}"):
                    df = df.drop(index=idx).reset_index(drop=True)
                    save_data(df)
                    st.experimental_rerun()
            st.divider()
    
    # 显示统计信息
    st.markdown("### 任务统计")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("总任务数", len(df))
    with col2:
        st.metric("已完成", len(completed_tasks))
    with col3:
        st.metric("未完成", len(incomplete_tasks))

if __name__ == "__main__":
    main()
