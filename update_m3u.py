import requests
import re

sources = [
    {"url": "https://raw.githubusercontent.com/andone1122/myIPTV/main/ipv6.m3u", "name": "原仓库频道"},
    {"url": "https://php.946985.filegear-sg.me/test.m3u", "name": "新增加频道组"}
]

def main():
    # 模拟真实浏览器的请求头
  headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://php.946985.filegear-sg.me/', # 增加来源伪装
        'Connection': 'keep-alive',
    }

    with open("merged.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for source in sources:
            try:
                # 加入 headers 伪装，并跳过 SSL 验证 (verify=False)
                response = requests.get(source["url"], headers=headers, timeout=30, verify=False)
                response.raise_for_status()
                
                content = response.text
                if not content.strip():
                    print(f"警告: {source['name']} 返回内容为空")
                    continue
                
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#EXTM3U"):
                        continue
                    
                    # 自动补全 group-title
                    if line.startswith("#EXTINF") and 'group-title="' not in line:
                        if "#EXTINF:-1," in line:
                            line = line.replace("#EXTINF:-1,", f'#EXTINF:-1 group-title="{source["name"]}",')
                        elif "#EXTINF:0," in line:
                            line = line.replace("#EXTINF:0,", f'#EXTINF:0 group-title="{source["name"]}",')
                    
                    f.write(line + "\n")
                print(f"成功合并: {source['name']}")
            except Exception as e:
                print(f"合并 {source['name']} 失败，错误原因: {e}")

if __name__ == "__main__":
    main()
