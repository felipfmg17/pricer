SELECT a.date_time_sec as Seconds, a.date_time as Date, b.name as "Currency Pair" , c.name as Exchange , a.price as Price
FROM coin_price as a
JOIN currency_pair as b
ON a.currency_pair_id = b.id
JOIN exchange as c
ON a.exchange_id = c.id
WHERE c.name = 'bitso'
AND b.name = 'btc_mxn';


SELECT a.date_time_sec as Seconds, a.date_time as Date, b.name as "Currency Pair" , c.name as Exchange , a.price as Price
FROM coin_price as a
JOIN currency_pair as b
ON a.currency_pair_id = b.id
JOIN exchange as c
ON a.exchange_id = c.id
WHERE c.name = 'bitfinex'
AND b.name = 'xrp_usd';


SELECT a.date_time_sec as Seconds, a.date_time as Date, b.name as "Currency Pair" , c.name as Exchange , a.price as Price
FROM coin_price as a
JOIN currency_pair as b
ON a.currency_pair_id = b.id
JOIN exchange as c
ON a.exchange_id = c.id
WHERE c.name = 'binance'
AND b.name = 'vibe_btc';