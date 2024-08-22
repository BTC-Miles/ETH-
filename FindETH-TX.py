import tkinter as tk
import threading
from web3 import Web3

def start_search():
    # 更新状态为"查找中"
    if not address_entry.get() or not start_block_entry.get() or not end_block_entry.get():
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "The input cannot be empty,Please reenter\n")
        return
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "Searching...ETH search efficiency is low, please wait\n")
    
    # 禁用搜索按钮，防止重复点击
    search_button.config(state=tk.DISABLED)
    
    address = address_entry.get()
    start_block = int(start_block_entry.get())
    end_block = int(end_block_entry.get())
    
    # 启动新的线程以避免阻塞GUI
    search_thread = threading.Thread(target=perform_search, args=(address, start_block, end_block))
    search_thread.start()

def perform_search(address, start_block, end_block):
    transactions = get_transactions(address, start_block, end_block)
    
    # 使用 after 方法将结果更新到主线程的 GUI 中
    output_text.after(0, update_output, transactions)

def update_output(transactions):
    output_text.delete(1.0, tk.END)  # 清空输出框
    if transactions:
        for tx in transactions:
            output_text.insert(tk.END, f"Transaction hash: {tx['hash'].hex()}\n")
            output_text.insert(tk.END, f"From: {tx['from']}, To: {tx['to']}\n")
            output_text.insert(tk.END, f"Value: {web3.from_wei(tx['value'], 'ether')} ETH\n")
            output_text.insert(tk.END, f"Block Number: {tx['blockNumber']}\n")
            output_text.insert(tk.END, f"Gas Used: {tx['gas']}\n")
            output_text.insert(tk.END, f"Gas Price: {web3.from_wei(tx['gasPrice'], 'gwei')} Gwei\n")
            output_text.insert(tk.END, "-" * 60 + "\n")
    else:
        output_text.insert(tk.END, "No transactions found.\n")
    
    # 查找完成后，恢复按钮状态
    search_button.config(state=tk.NORMAL)

def get_transactions(address, start_block, end_block):
    transactions = []
    latest_block = web3.eth.block_number
    if end_block > latest_block:
        end_block = latest_block  # 确保终止区块不超过最新区块

    for block_num in range(start_block, end_block + 1):
        block = web3.eth.get_block(block_num, full_transactions=True)
        for tx in block.transactions:
            if tx['from'].lower() == address.lower() or (tx['to'] and tx['to'].lower() == address.lower()):
                transactions.append(tx)

    return transactions

# 设置以太坊节点连接
infura_url = "https://mainnet.infura.io/v3/860b13c04ecb4dcb9080a8887ba1b446"
web3 = Web3(Web3.HTTPProvider(infura_url))

# 创建主窗口
root = tk.Tk()
root.title("Ethereum Transaction Finder")
root.geometry("600x450")  # 增加窗口高度

# 地址输入框
tk.Label(root, text="Enter Ethereum Address:").grid(row=0, column=0, pady=10, padx=10, sticky="w")
address_entry = tk.Entry(root, width=50)
address_entry.grid(row=1, column=0, pady=5, padx=10)

# 起始区块输入框
tk.Label(root, text="Start Block:").grid(row=2, column=0, pady=10, padx=10, sticky="w")
start_block_entry = tk.Entry(root, width=20)
start_block_entry.grid(row=3, column=0, pady=5, padx=10, sticky="w")

# 终止区块输入框
tk.Label(root, text="End Block:").grid(row=2, column=1, pady=10, padx=10, sticky="w")
end_block_entry = tk.Entry(root, width=20)
end_block_entry.grid(row=3, column=1, pady=5, padx=10, sticky="w")

# 开始搜索按钮
search_button = tk.Button(root, text="Start Search", command=start_search)
search_button.grid(row=4, column=0, pady=10, padx=10)

# 输出文本框
output_text = tk.Text(root, wrap='word', height=15, width=70) 
output_text.grid(row=5, column=0, pady=10, padx=10, columnspan=2, sticky="nsew")

# 让窗口中的元素填充并扩展
root.grid_rowconfigure(5, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# 运行主循环
root.update_idletasks()  # 强制刷新窗口
root.mainloop()
