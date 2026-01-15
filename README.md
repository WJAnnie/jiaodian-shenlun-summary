# 焦点访谈申论总结

每天自动获取央视《焦点访谈》最新一期 → AI生成评论性申论文章 → 推送到微信

## 生成文章格式

- **标题**：简洁有力，体现文章核心观点
- **第一段**（约200字）：背景引入，最后一句为总论点
- **第二至四段**（各约250字）：三个分论点，每段首句对仗工整
- **第五段**（约100字）：总结升华，呼应全文

### 写作特点
- 案例简短（30-50字），道理论证充分
- 名言引用来自中国古语或习近平讲话
- 举例论证与道理论证相结合

## 部署步骤

### 1. 创建 GitHub 仓库

1. 登录 GitHub，点击右上角 `+` → `New repository`
2. 仓库名填 `jiaodian-shenlun-summary`（或其他名字）
3. 选择 `Private`（私有）
4. 点击 `Create repository`

### 2. 上传代码

在本地 `D:\ClaudeFile\焦点访谈申论总结` 目录运行：

```bash
git init
git add .
git commit -m "初始化"
git branch -M main
git remote add origin https://github.com/你的用户名/jiaodian-shenlun-summary.git
git push -u origin main
```

### 3. 配置 Secrets

1. 进入仓库页面，点击 `Settings` → `Secrets and variables` → `Actions`
2. 点击 `New repository secret`，添加：
   - Name: `SERVERCHAN_KEY`
   - Value: 你的Server酱Key
3. 再添加一个：
   - Name: `DEEPSEEK_API_KEY`
   - Value: 你的DeepSeek API Key

### 4. 启用 Actions

1. 点击仓库的 `Actions` 标签
2. 点击 `I understand my workflows, go ahead and enable them`
3. 手动测试：点击左侧 `每日焦点访谈申论总结` → `Run workflow` → `Run workflow`

### 5. 完成

每天上午 9:00，你会自动收到微信推送！

## 修改推送时间

编辑 `.github/workflows/daily.yml`：

```yaml
- cron: '0 1 * * *'  # UTC时间，北京时间 = UTC + 8
```

常用时间（北京时间）：
- 09:00 → `0 1 * * *`
- 21:00 → `0 13 * * *`
- 22:00 → `0 14 * * *`
- 08:00 → `0 0 * * *`

## 本地测试

```bash
set SERVERCHAN_KEY=你的key
set DEEPSEEK_API_KEY=你的key
python main.py
```
