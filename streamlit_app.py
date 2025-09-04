import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import time
import numpy as np
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="CPU性能指標可視化学習アプリ",
    page_icon="💻",
    layout="wide"
)

# Title and credits
st.title("💻 CPU性能指標可視化学習アプリ")
st.caption("Created by Dit-Lab.(Daiki ITO)")
st.caption("Supported by Tomoaki ATSUMI")

st.markdown("---")
st.markdown("### CPUの性能指標を体験的に学ぼう！")
st.markdown("このアプリでは、**ビット数**と**クロック周波数**がCPUの性能にどのように影響するかを視覚的に理解できます。")

# Section 1: Bit Width and Data Processing
st.markdown("---")
st.markdown("## 🔢 1. ビット数とデータ処理能力")
st.markdown("CPUのビット数は、一度に処理できるデータの幅を決定します。")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### ビット数を選択:")
    bit_width = st.radio(
        "CPUのビット数",
        options=[32, 64],
        format_func=lambda x: f"{x}ビットCPU",
        key="bit_width"
    )
    
    st.markdown("### 処理するデータ:")
    sample_data = "1234567890ABCDEF"
    st.code(sample_data, language="text")
    
    # データサイズの説明
    data_size = len(sample_data)
    st.write(f"データサイズ: {data_size} バイト")
    
    if st.button("データ処理をシミュレート", key="simulate_data_btn"):
        st.session_state.simulate_data_state = True

with col2:
    if st.session_state.get('simulate_data_state', False):
        st.markdown("### 処理過程の可視化")
        
        # データを分割
        bytes_per_cycle = bit_width // 8
        chunks = [sample_data[i:i+bytes_per_cycle] for i in range(0, len(sample_data), bytes_per_cycle)]
        
        # 処理時間の計算（シミュレーション）
        total_cycles = len(chunks)
        processing_time = total_cycles * 0.5  # 仮想的な処理時間
        
        # アニメーションのプロット
        fig = go.Figure()
        
        # データチャンクの表示
        for i, chunk in enumerate(chunks):
            fig.add_trace(go.Bar(
                x=[f"サイクル {i+1}"],
                y=[len(chunk)],
                name=f"チャンク: {chunk}",
                text=chunk,
                textposition="auto",
                marker_color=f"rgba({50 + i*30}, {150 + i*20}, {200 + i*10}, 0.8)"
            ))
        
        fig.update_layout(
            title=f"{bit_width}ビットCPU: データ処理の様子",
            xaxis_title="処理サイクル",
            yaxis_title="処理データ量 (バイト)",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 結果の説明
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("処理サイクル数", f"{total_cycles}")
        with col_b:
            st.metric("1サイクルあたりのデータ量", f"{bytes_per_cycle} バイト")
        with col_c:
            st.metric("推定処理時間", f"{processing_time:.1f} 秒")

# Section 2: Clock Frequency and Processing Speed
st.markdown("---")
st.markdown("## ⚡ 2. クロック周波数と処理速度")
st.markdown("CPUのクロック周波数は、1秒間に実行できる処理回数を決定します。")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### クロック周波数を設定:")
    frequency_ghz = st.slider(
        "クロック周波数 (GHz)",
        min_value=1.0,
        max_value=5.0,
        value=2.5,
        step=0.5,
        format="%.1f GHz",
        key="frequency"
    )
    
    st.markdown("### シミュレーション設定:")
    task_count = st.slider(
        "処理するタスク数",
        min_value=5,
        max_value=20,
        value=10,
        key="task_count"
    )
    
    if st.button("処理速度をシミュレート", key="simulate_speed_btn"):
        st.session_state.simulate_speed_state = True
        st.session_state.frequency_value = frequency_ghz
        st.session_state.task_count_value = task_count

with col2:
    if st.session_state.get('simulate_speed_state', False):
        st.markdown("### 処理速度シミュレーション")
        
        freq = st.session_state.frequency_value
        tasks = st.session_state.task_count_value
        
        # 処理時間の計算
        base_time_per_task = 1.0  # 1GHzでの基準時間（秒）
        time_per_task = base_time_per_task / freq
        total_time = tasks * time_per_task
        
        # タスク完了のタイムライン
        completion_times = [i * time_per_task for i in range(1, tasks + 1)]
        
        # アニメーション風のプロット
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=("タスク完了状況", "処理時間の比較"),
            specs=[[{"secondary_y": False}], [{"secondary_y": False}]],
            vertical_spacing=0.15
        )
        
        # タスク完了のバープロット
        fig.add_trace(
            go.Bar(
                x=[f"タスク{i+1}" for i in range(tasks)],
                y=[1]*tasks,
                marker_color=['green' if completion_times[i] <= total_time else 'red' for i in range(tasks)],
                name="完了タスク",
                text=[f"{completion_times[i]:.2f}s" for i in range(tasks)],
                textposition="auto"
            ),
            row=1, col=1
        )
        
        # 異なる周波数での比較
        frequencies = [1.0, 2.0, 3.0, 4.0, 5.0]
        processing_times = [tasks * base_time_per_task / f for f in frequencies]
        
        fig.add_trace(
            go.Scatter(
                x=frequencies,
                y=processing_times,
                mode='lines+markers',
                name="処理時間",
                line=dict(color='blue', width=3),
                marker=dict(size=8, symbol='circle')
            ),
            row=2, col=1
        )
        
        # 現在の設定をハイライト
        fig.add_trace(
            go.Scatter(
                x=[freq],
                y=[total_time],
                mode='markers',
                name="現在の設定",
                marker=dict(size=15, color='red', symbol='star')
            ),
            row=2, col=1
        )
        
        fig.update_xaxes(title_text="タスク", row=1, col=1)
        fig.update_yaxes(title_text="完了状態", row=1, col=1)
        fig.update_xaxes(title_text="クロック周波数 (GHz)", row=2, col=1)
        fig.update_yaxes(title_text="総処理時間 (秒)", row=2, col=1)
        
        fig.update_layout(
            height=600,
            title_text=f"クロック周波数 {freq}GHz での処理シミュレーション"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 結果の説明
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("クロック周波数", f"{freq:.1f} GHz")
        with col_b:
            st.metric("1タスクあたりの時間", f"{time_per_task:.3f} 秒")
        with col_c:
            st.metric("総処理時間", f"{total_time:.2f} 秒")

# Section 3: Performance Comparison
st.markdown("---")
st.markdown("## 📊 3. 性能比較と最適化")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### CPU性能の組み合わせ効果")
    
    # 性能マトリックス
    bit_options = [32, 64]
    freq_options = [1.5, 2.5, 3.5, 4.5]
    
    performance_matrix = []
    for bits in bit_options:
        row = []
        for freq in freq_options:
            # 仮想的な性能スコア計算
            data_throughput = (bits / 32) * freq
            performance_score = data_throughput * 100
            row.append(performance_score)
        performance_matrix.append(row)
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=performance_matrix,
        x=[f"{f}GHz" for f in freq_options],
        y=[f"{b}bit" for b in bit_options],
        colorscale='Viridis',
        text=[[f"{score:.0f}" for score in row] for row in performance_matrix],
        texttemplate="%{text}",
        textfont={"size": 12},
        colorbar=dict(title="性能スコア")
    ))
    
    fig_heatmap.update_layout(
        title="CPU性能マトリックス",
        xaxis_title="クロック周波数",
        yaxis_title="ビット数",
        height=300
    )
    
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col2:
    st.markdown("### 実世界での性能差")
    
    # 実際のタスクでの性能比較
    tasks = ["文書処理", "画像編集", "動画変換", "ゲーム", "AI計算"]
    cpu_32bit_2ghz = [5.2, 15.8, 45.3, 25.7, 120.5]
    cpu_64bit_4ghz = [2.1, 6.2, 18.9, 10.3, 35.2]
    
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Bar(
        name='32bit 2GHz',
        x=tasks,
        y=cpu_32bit_2ghz,
        marker_color='lightblue'
    ))
    
    fig_comparison.add_trace(go.Bar(
        name='64bit 4GHz',
        x=tasks,
        y=cpu_64bit_4ghz,
        marker_color='darkblue'
    ))
    
    fig_comparison.update_layout(
        title='実世界タスクでの処理時間比較',
        xaxis_title='タスク種類',
        yaxis_title='処理時間 (秒)',
        barmode='group',
        height=300
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)

# Section 4: Interactive Learning Section
st.markdown("---")
st.markdown("## 🎯 4. インタラクティブ学習")

tab1, tab2, tab3 = st.tabs(["クイズ", "性能計算器", "実験ラボ"])

with tab1:
    st.markdown("### CPU性能クイズ")
    
    quiz_questions = [
        {
            "question": "64ビットCPUが32ビットCPUより優れている理由は？",
            "options": ["クロックが速い", "一度により多くのデータを処理できる", "消費電力が少ない", "価格が安い"],
            "correct": 1,
            "explanation": "64ビットCPUは一度に64ビット（8バイト）のデータを処理できるため、32ビット（4バイト）のCPUより効率的です。"
        },
        {
            "question": "クロック周波数が2倍になると処理速度は？",
            "options": ["変わらない", "約2倍速くなる", "4倍速くなる", "半分になる"],
            "correct": 1,
            "explanation": "クロック周波数が2倍になると、理論的には処理速度も約2倍になります。"
        }
    ]
    
    for i, q in enumerate(quiz_questions):
        st.markdown(f"**問題{i+1}:** {q['question']}")
        answer = st.radio(f"選択肢_{i}", q["options"], key=f"quiz_{i}")
        if st.button(f"答えを確認", key=f"check_{i}"):
            if q["options"].index(answer) == q["correct"]:
                st.success("正解！ ✅")
            else:
                st.error("不正解 ❌")
            st.info(f"解説: {q['explanation']}")

with tab2:
    st.markdown("### CPU性能計算器")
    
    col_calc1, col_calc2 = st.columns(2)
    
    with col_calc1:
        st.markdown("#### CPU仕様を入力:")
        calc_bits = st.selectbox("ビット数", [16, 32, 64], index=1, key="calc_bits")
        calc_freq = st.number_input("クロック周波数 (GHz)", min_value=0.5, max_value=6.0, value=3.0, step=0.1, key="calc_freq")
        calc_cores = st.number_input("コア数", min_value=1, max_value=16, value=4, key="calc_cores")
    
    with col_calc2:
        st.markdown("#### 計算結果:")
        
        # 仮想的な性能計算
        base_performance = (calc_bits / 32) * calc_freq * calc_cores
        single_thread_score = base_performance * 100
        multi_thread_score = base_performance * calc_cores * 85  # 85%効率と仮定
        
        st.metric("シングルスレッド性能", f"{single_thread_score:.0f}")
        st.metric("マルチスレッド性能", f"{multi_thread_score:.0f}")
        st.metric("データ処理能力", f"{calc_bits * calc_freq:.1f} bit/sec")

with tab3:
    st.markdown("### 実験ラボ")
    
    st.markdown("#### ワークロードシミュレーション")
    
    workload_type = st.selectbox(
        "ワークロードの種類",
        ["CPU集約的", "メモリ集約的", "I/O集約的", "並列処理"],
        key="workload"
    )
    
    data_size = st.slider("データサイズ (MB)", 1, 1000, 100, key="data_size")
    
    if st.button("シミュレーション実行", key="run_simulation"):
        # ワークロード別の性能特性
        workload_factors = {
            "CPU集約的": {"cpu_weight": 0.8, "memory_weight": 0.1, "io_weight": 0.1},
            "メモリ集約的": {"cpu_weight": 0.3, "memory_weight": 0.6, "io_weight": 0.1},
            "I/O集約的": {"cpu_weight": 0.2, "memory_weight": 0.2, "io_weight": 0.6},
            "並列処理": {"cpu_weight": 0.7, "memory_weight": 0.2, "io_weight": 0.1}
        }
        
        factor = workload_factors[workload_type]
        
        # 異なるCPU構成での予想性能
        configs = [
            {"name": "Entry Level", "bits": 32, "freq": 2.0, "cores": 2},
            {"name": "Mid Range", "bits": 64, "freq": 3.0, "cores": 4},
            {"name": "High End", "bits": 64, "freq": 4.5, "cores": 8},
            {"name": "Workstation", "bits": 64, "freq": 3.8, "cores": 16}
        ]
        
        results = []
        for config in configs:
            cpu_score = config["bits"] * config["freq"] * config["cores"] / 100
            performance = (cpu_score * factor["cpu_weight"] + 
                         config["cores"] * factor["memory_weight"] + 
                         config["freq"] * factor["io_weight"])
            processing_time = data_size / max(performance, 0.1)  # MB/s換算
            results.append({
                "構成": config["name"],
                "性能スコア": performance,
                "予想処理時間": processing_time
            })
        
        df_results = pd.DataFrame(results)
        
        fig_sim = px.bar(df_results, x="構成", y="予想処理時間", 
                        title=f"{workload_type}ワークロード ({data_size}MB) の処理時間予測")
        st.plotly_chart(fig_sim, use_container_width=True)
        
        st.dataframe(df_results, use_container_width=True)

# Section 5: Summary and Insights
st.markdown("---")
st.markdown("## 🎓 5. まとめと考察")

col_summary1, col_summary2 = st.columns(2)

with col_summary1:
    st.markdown("""
    ### 🔑 重要なポイント
    
    **ビット数の影響:**
    - 一度に処理できるデータの幅を決定
    - 64ビットは32ビットの2倍のデータを同時処理
    - メモリアドレス空間も大幅に拡大
    
    **クロック周波数の影響:**
    - 1秒間に実行できる処理回数を決定
    - 周波数が2倍 → 処理速度も約2倍
    - 発熱と消費電力とのトレードオフ
    
    **総合性能:**
    - ビット数 × クロック周波数 × コア数
    - ワークロードによって最適な構成が異なる
    """)

with col_summary2:
    st.markdown("""
    ### 🚗 車との比較で理解
    
    **ビット数 = 車の積載能力**
    - 32ビット = 軽トラック (4バイト)
    - 64ビット = 大型トラック (8バイト)
    
    **クロック周波数 = エンジン回転数**
    - 高回転 = 高速処理
    - 燃費（消費電力）との兼ね合い
    
    **コア数 = 車両台数**
    - マルチコア = 複数台での並列作業
    - 作業の種類によって効果が変わる
    """)

# Interactive performance predictor
st.markdown("---")
st.markdown("### 🔮 性能予測ツール")

pred_col1, pred_col2, pred_col3 = st.columns(3)

with pred_col1:
    pred_bits = st.selectbox("ビット数", [32, 64], key="pred_bits")
    pred_freq = st.slider("クロック周波数 (GHz)", 1.0, 5.0, 3.0, key="pred_freq")

with pred_col2:
    pred_cores = st.slider("コア数", 1, 16, 4, key="pred_cores")
    pred_workload = st.selectbox("主な用途", 
                                ["オフィス作業", "プログラミング", "ゲーミング", "動画編集", "AI・機械学習"],
                                key="pred_workload")

with pred_col3:
    # 性能予測計算
    base_score = (pred_bits/32) * pred_freq * pred_cores
    workload_multipliers = {
        "オフィス作業": 0.5, "プログラミング": 0.7, "ゲーミング": 1.0,
        "動画編集": 1.3, "AI・機械学習": 1.8
    }
    final_score = base_score * workload_multipliers[pred_workload] * 100
    
    st.metric("予測性能スコア", f"{final_score:.0f}")
    
    if final_score < 300:
        st.warning("⚠️ 軽い作業向け")
    elif final_score < 600:
        st.info("ℹ️ 一般的な作業に適している")
    elif final_score < 1000:
        st.success("✅ 高性能、重い作業も快適")
    else:
        st.success("🚀 ワークステーション級の性能")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
<p>このアプリケーションを通じて、CPUの性能指標が単なる数値ではなく、<br>
コンピュータの処理能力を決定づける重要な要因であることを理解していただけたでしょうか。</p>
<p><small>CPU性能の理解は、最適なコンピュータ選択や性能最適化の第一歩です。</small></p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'simulate_data_state' not in st.session_state:
    st.session_state.simulate_data_state = False
if 'simulate_speed_state' not in st.session_state:
    st.session_state.simulate_speed_state = False