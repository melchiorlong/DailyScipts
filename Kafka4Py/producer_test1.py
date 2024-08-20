from kafka import KafkaProducer

# 创建 Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# 读取文件内容
file_path = 'example.txt'
with open(file_path, 'rb') as file:
    file_content = file.read()

# 发送文件内容到 Kafka 主题
producer.send('file_topic', key=b'file_key', value=file_content)
producer.flush()

print(f"File {file_path} sent to Kafka topic 'file_topic'.")
