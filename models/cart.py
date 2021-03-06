from cachelib import SimpleCache
from linebot.models import *
from database import db_session
from models.product import Products

cache = SimpleCache()


class Cart(object):
    def __init__(self, user_id):
        self.cache = cache
        self.user_id = user_id

    def bucket(self):
        return cache.get(key=self.user_id) or {}

    def add(self, product, num):
        bucket = cache.get(key=self.user_id)
        if bucket == None:
            cache.add(key=self.user_id, value={product: int(num)})
        else:
            bucket.update({product: int(num)})
            cache.set(key=self.user_id, value=bucket)

    def reset(self):
        cache.set(key=self.user_id, value={})

    # 顯示購物車
    def display(self):
        total = 0
        product_box_component = []

        for product_name, num in self.bucket().items():
            product = db_session.query(Products).filter(Products.name.ilike(product_name)).first()
            amount = product.price * int(num)
            total += amount

            product_box_component.append(BoxComponent(
                layout='horizontal',
                contents=[
                    TextComponent(text='{num} x {product}'.format(num=num, product=product_name),
                                  size='sm', color='#555555', flex=1),
                    TextComponent(text='NT$ {amount}'.format(amount=amount),
                                  size='sm', color='#111111', align='end')]
            ))

        bublle = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='以下是您的訂單',
                                  wrap=True,
                                  size='md'),
                    SeparatorComponent(margin='xxl'),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=product_box_component
                    ),
                    SeparatorComponent(margin='xxl'),
                    BoxComponent(
                        layout='vertical',
                        margin='xxl',
                        spacing='sm',
                        contents=[
                            TextComponent(text='TATAL',
                                          size='sm',
                                          color='#555555',
                                          flex=0),
                            TextComponent(text='NT$ {total}'.format(total=total),
                                          size='sm',
                                          color='#111111',
                                          align='end')]
                    )
                ]
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='md',
                contents=[
                    ButtonComponent(
                        style='primary',
                        color='#1DB446',
                        action=PostbackAction(label='Checkout',
                                              data='action=checkout')
                    ),
                    BoxComponent(
                        layout='horizontal',
                        spacing='md',
                        contents=[
                            ButtonComponent(
                                style='primary',
                                color='#aaaaaa',
                                flex=3,
                                action=PostbackAction(label='清空購物車',
                                                      text='清空購物車',
                                                      data='Empty Cart')
                            ),
                            ButtonComponent(
                                style='primary',
                                color='#aaaaaa',
                                flex=2,
                                action=PostbackAction(label='Add',
                                                      text='朕還能點',
                                                      data='add')
                            )
                        ]
                    )
                ]
            )
        )

        message = FlexSendMessage(alt_text='這是您的購物清單', contents=bublle)

        return message
