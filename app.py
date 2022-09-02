from flask import Flask,request
from binance.client import Client


app = Flask(__name__)


bidding_p = 0
current = 0







def start_bot(data):
        # authenticated = request.session.get('authenticated')
        # if authenticated==False:
        #     return JsonResponse({"status": False, "message": "Please Login To Use The App"})
        class test_class:
            client=''
            bidding=''
            tradeA = False
            tradeB = False
            user = ""

        api_key = data['api_key']
        secret_key = data['secret_key']
        client = Client(api_key,secret_key)
        test_class.client=client
        # client = request.session.get('client')
        def place_order(side, quantity,price, symbol):
            try:
                order = test_class.client.create_order(
                symbol=symbol,
                side=side,
                type=ORDER_TYPE_LIMIT,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=str(price)
                )
                print(order)
                
                Order.objects.create(order)
            except BinanceAPIException as ex:
                print(f"{ex}")
            return order
            #
        while True:
            symbol="XRPUSDT"
            try:
                current_price = float(test_class.client.get_symbol_ticker(symbol=symbol)["price"])
                current_price =float('{:.8f}'.format(current_price))
                print(current_price)
                if test_class.bidding == '':
                    test_class.bidding = current_price
                    # order = place_order(SIDE_BUY,30,current_price,symbol)
                    print(current_price)
#		    bidding_p = current_price
                    # print(f"Buy Order : {order}")
                else:
                    previous_price = test_class.bidding
                    per5 = float(previous_price)*5/100
                    per5_profit = float(previous_price) + per5
#		    current = current_price
                    # per1 = float(previous_price)/100 # 0.5 percent profit
                    # per10 = (float(previous_price)*10)/100
                    # per1 = float('{:.8f}'.format(per1))
                    # per10 = float('{:.8f}'.format(per10))
                    # per1_profit = float(previous_price) + per1
                    # per1_profit = float('{:.8f}'.format(per1_profit))
                    # per1_loss = float(previous_price) - per1
                    # per1_loss = float('{:.8f}'.format(per1_loss))
                    # per10_loss = float(previous_price) - per10
                    # per10_loss = float('{:.8f}'.format(per10_loss))
                    print("Current Price : ",current_price)
                    # print("One Perc : ",per1 )
                    # print("Ten Perc : ", per10)
                    # print("Per1 Profit : ",per1_profit,"Per1 Loss : ",per1_loss,"Per10 Loss : ",per10_loss)
                    if float(current_price) >= per5_profit and test_class.tradeA==False :
                        print("***sell***")
                        print(current_price)
                        test_class.tradeA=True
                        test_class.bidding = current_price
                        order = place_order(SIDE_SELL, 29, current_price, symbol)
                        print(f"{order}:::current_price{current_price}")
                        break
                #     elif current_price <= per1_loss and test_class.tradeB==False:
                #         print("buy")
                #         print(current_price)
                #         test_class.tradeB = True
                #         test_class.tradeA=False
                #         test_class.bidding = current_price
                #         order = place_order(SIDE_BUY, 30, current_price, symbol)
                # #         order(SIDE_BUY,10,current_price,symbol)
                # #         buy_counter+=1
                # #         print(f"BidPrice{bid_price}:::current_price{current_price}")
                #     elif current_price < per10_loss  and test_class.tradeB:

                #         order_sell = place_order(SIDE_SELL, 29, current_price, symbol)
                #         sleep(30*60)
                #         current_price = float(test_class.client.get_symbol_ticker(symbol=symbol)["price"])
                #         current_price =float('{:.8f}'.format(current_price))
                #         order_buy = place_order(SIDE_BUY, 30, current_price, symbol)

                #         print(f"Order Sell : {order_sell}, Order Buy : {order_buy}")
                #         test_class.bidding = current_price
                #         print(current_price)
                #         test_class.tradeB = False

            except Exception as ex:
                print(f"{ex}")
                return JsonResponse({"Error":f"{ex}"})
            sleep(3)
        return {"data":{"current price":current_price,"Last Price":test_class.bidding}}

@app.route('/start',methods=["POST"])
def start():
	data = request.get_dict()
	data = start_bot()

	return

@app.route('/show',methods=["GET"])
def show():
	return {"Old Price":budding_p,"Current Price":current}


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=8000,debug=True)
