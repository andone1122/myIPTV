import requests
import re

# 定义需要合并的源
sources = [
    {"url": "https://raw.githubusercontent.com/andone1122/myIPTV/main/ipv6.m3u", "name": "原仓库频道"},
    {"url": "https://php.946985.filegear-sg.me/test.m3u", "港澳测试频道": "新增加频道组"}
]

def main():
    with open("merged.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for source in sources:
            try:
                response = requests.get(source["url"], timeout=15)
                response.raise_for_status()
                content = response.text
                
                # 移除每个文件的 #EXTM3U 头部，避免重复
                lines = content.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith("#EXTM3U"):
                        continue
                    
                    # 关键步骤：强制给新加入的源添加 group-title 分组
                    if line.startswith("#EXTINF") and 'group-title="' not in line:
                        line = line.replace("#EXTINF:-1,", f'#EXTINF:-1 group-title="{source["name"]}",')
                        line = line.replace("#EXTINF:0,", f'#EXTINF:0 group-title="{source["name"]}",')
                    
                    f.write(line + "\n")
                print(f"成功合并: {source['name']}")
            except Exception as e:
                print(f"合并 {source['name']} 失败: {e}")

if __name__ == "__main__":
    main()
