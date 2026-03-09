import requests
import urllib3

# 禁用安全请求警告（因为我们要跳过SSL验证）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sources = [
    {"url": "https://raw.githubusercontent.com/andone1122/myIPTV/main/ipv6.m3u", "name": "原仓库频道"},
    {"url": "https://php.946985.filegear-sg.me/test.m3u", "name": "新增加频道组"}
]

def main():
    # 模拟更真实、更高权重的浏览器请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'https://php.946985.filegear-sg.me/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    print("开始执行合并任务...")
    
    with open("merged.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for source in sources:
            try:
                print(f"正在抓取: {source['name']}...")
                # 加入 verify=False 解决证书问题，加入 headers 绕过初步拦截
                response = requests.get(source["url"], headers=headers, timeout=30, verify=False)
                
                if response.status_code == 403:
                    print(f"错误: {source['name']} 拒绝访问 (403 Forbidden)。这通常是由于 GitHub 服务器 IP 被封。")
                    continue
                
                response.raise_for_status()
                
                lines = response.text.split('\n')
                count = 0
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#EXTM3U"):
                        continue
                    
                    if line.startswith("#EXTINF") and 'group-title="' not in line:
                        line = line.replace("#EXTINF:-1,", f'#EXTINF:-1 group-title="{source["name"]}",')
                        line = line.replace("#EXTINF:0,", f'#EXTINF:0 group-title="{source["name"]}",')
                    
                    f.write(line + "\n")
                    count += 1
                print(f"成功合并: {source['name']} (共 {count} 行内容)")
            except Exception as e:
                print(f"无法获取 {source['name']}，跳过。错误详情: {e}")

if __name__ == "__main__":
    main()
