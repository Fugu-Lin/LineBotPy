from sqlalchemy import Column, DateTime, String, Integer, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from linebot.models import *
from database import Base


class Orders(Base):
    __tablename__ = 'orders'

    # id為主鍵
    id = Column(String, primary_key=True)
    # 訂單總金額
    amount = Column(Integer)
    # linepay用
    transaction_id = Column(String)
    # 是否付款
    is_pay = Column(Boolean, default=False)
    # 訂單建立時間
    created_time = Column(DateTime, default=func.now())
    # 加入user.id為外來鍵
    user_id = Column("user_id", ForeignKey("users.id"))
    # 加上與items的關聯性
    items = relationship('Items', backref='order')

    # 關聯性示意

    # order.items
    # [<Item 1>, <Item 2>]

    # item.order
    # <Order 1>

    def display_receipt(self):
        item_box_component = []

        for item in self.items:
            item_box_component.append(BoxComponent(
                layout='horizontal',
                contents=[
                    TextComponent(text='{quantity} x {product_name}'.
                                  format(quantity=item.quantity,
                                         product_name=item.product_name),
                                  size='sm',
                                  color='#555555',
                                  flex=0),
                    TextComponent(text='NT${amount}'.
                                  format(amount=(item.quantity * item.product_price)),
                                  size='sm',
                                  color='#111111',
                                  align='end')]
            ))

        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='RECEIPT',
                                  weight='bold',
                                  color='#1DB446',
                                  size='sm'),
                    TextComponent(text='OrderBot 點吧',
                                  weight='bold',
                                  size='xxl',
                                  margin='md'),
                    TextComponent(text='Online Store',
                                  size='xs',
                                  color='#aaaaaa',
                                  wrap=True),
                    SeparatorComponent(margin='xxl'),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=item_box_component
                    ),
                    SeparatorComponent(margin='xxl'),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='horizontal',
                                contents=[
                                    TextComponent(text='TOTAL',
                                                  size='sm',
                                                  color='#555555',
                                                  flex=0),
                                    TextComponent(text='NT${total}'.
                                                  format(total=self.amount),
                                                  size='sm',
                                                  color='#111111',
                                                  align='end')]
                            )

                        ]
                    )
                ],
            )
        )

        message = FlexSendMessage(alt_text='receipt', contents=bubble)

        return message
