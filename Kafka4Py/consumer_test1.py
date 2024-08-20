from kafka import KafkaConsumer

# 创建 Kafka Consumer
consumer = KafkaConsumer('file_topic', bootstrap_servers='localhost:9092', auto_offset_reset='earliest')

# 接收消息并写入文件
for message in consumer:
    with open('received_example.txt', 'wb') as file:
        file.write(message.value)
    print("File received and written to 'received_example.txt'.")
    break  # 仅处理一个文件后退出
