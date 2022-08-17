# AGV RL Negotiation Real and Sim

AISTでの実証実験を反映して、強化学習を用いた自動交渉アルゴリズム評価環境構築。
今年度まではシミュレーション上での評価を完了。来年度に実機側を動かすエンジンとの簡易接続まで行う予定。

# Problem Setting
webブラウザを利用したインタラクティブなシミュレータ&pythonベースの学習エンジン(planner_demo.py)
![Fig](demo.png)

# Value Based Negotiation
We propose policy and Value based Utility function.

# Examples
Problem setting@AIST 
## Original Path
タスクに応じた、将来予測を反映した空間価値と経路計画

![Value_example](single_agent/agent1_value.gif)
### Agent1,RLで学習したモデルによる経路計画
![Agent1](single_agent/agent1.gif)
### Agent2, RLで学習したモデルによる経路計画
![Agent2](single_agent/agent2.gif)

### Without Negotiation
各エージェント(例えば、異なる企業間)で独自に学習すると、経路上で衝突が生じる。
各エージェントが最適経路を目指した結果、最悪のケースの例。
![](single_agent/agent_block.gif)

## Negotiated Path Planning RL
### Scinario1
エージェント２の企業が、自動で再経路計画を実行し、衝突を回避した場合。
モデルベース強化学習により、衝突を回避する経路を再導出できる。
![](single_agent/agent_sc1.gif)
### Scinario2
エージェント２がエージェント１に対して、SAOによる自動交渉を行った場合。
エージェント２の企業が優先的にタスクを完了させなければならない時、お互いにとってメリットがあるような取引を行うことができる。
![](single_agent/agent_sc2.gif)
