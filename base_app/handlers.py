from linebot import WebhookHandler


YOUR_CHANNEL_SECRET = 'c14023a94c9de74d28a555cd78079510'
# สร้าง Webhook Handler

handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# สร้างฟังก์ชันสำหรับการรับข้อความจาก LINE Bot
def handle_message(event):
    pass

# สร้างฟังก์ชันสำหรับการรับเหตุการณ์อื่นๆ จาก LINE Bot
def handle_event(event):
    pass
