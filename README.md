# Cyber Log Analyzer

一个面向网络安全日志分析场景的原创开源软件原型项目，支持日志读取、异常关键词识别、风险事件统计和结果导出，具备独立运行与命令行交互能力，可用于安全实验教学、课程演示和基础安全事件排查。

## 功能特性

- 日志文件读取与解析
- 异常关键词识别
- 风险事件统计与分级
- 结果导出为 JSON / CSV
- 命令行交互，便于快速集成与演示
- 配套样例数据、测试代码和默认规则配置

## 项目结构

```text
cyber-log-analyzer/
├── config/
│   └── default_keywords.json
├── data/
│   └── sample_security.log
├── security_log_analyzer/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── cli.py
│   ├── exporter.py
│   ├── parser.py
│   └── rules.py
├── tests/
│   └── test_analyzer.py
├── .gitignore
├── LICENSE
├── pyproject.toml
└── README.md
```

## 安装方式

### 方式一：直接运行

```bash
git clone <your-repo-url>
cd cyber-log-analyzer
python -m security_log_analyzer.cli --input data/sample_security.log --output report.json
```

### 方式二：本地安装命令行工具

```bash
pip install .
cyber-log-analyzer --input data/sample_security.log --output report.json
```

## 使用示例

### 基础分析

```bash
python -m security_log_analyzer.cli \
  --input data/sample_security.log \
  --output results.json
```

### 导出 CSV 明细

```bash
python -m security_log_analyzer.cli \
  --input data/sample_security.log \
  --output results.csv \
  --format csv
```

### 指定自定义关键词规则

```bash
python -m security_log_analyzer.cli \
  --input data/sample_security.log \
  --rules config/default_keywords.json \
  --output results.json
```

## 输入日志格式

工具默认支持常见文本日志，每行一条记录，推荐格式如下：

```text
2026-03-20 10:15:21 INFO auth-service User login success from 192.168.1.10
2026-03-20 10:17:42 WARN web-gateway SQL injection attempt detected from 10.0.0.8
2026-03-20 10:18:10 ERROR firewall Multiple failed login attempts from 172.16.0.3
```

若输入行无法完全匹配推荐格式，系统仍会保留原始文本并进行关键词识别。

## 输出内容

输出报告主要包含：

- 基础统计信息（总日志数、命中事件数、风险等级分布）
- 风险事件类别统计
- 命中明细（时间、级别、模块、风险分数、命中关键词、原始日志）

## 默认风险类别

- authentication：登录失败、暴力破解、未授权访问等
- malware：木马、病毒、恶意载荷等
- injection：SQL 注入、命令注入、脚本注入等
- reconnaissance：扫描、探测、枚举等
- exfiltration：数据泄露、数据导出、可疑外传等

## 测试运行

```bash
python -m unittest discover -s tests
```

## 适用场景

- 网络安全实验教学
- 安全日志分析课程原型展示
- 基础事件排查与演示
- 中期开源项目成果展示

## 后续可扩展方向

- 增加正则规则和 YARA / Sigma 风格检测能力
- 增加 Web 可视化分析界面
- 支持多种日志格式自动识别
- 对接数据库、消息队列和 SIEM 平台
- 丰富社区协作与开源治理文档

## 开源协议

本项目使用 MIT License。
