## Market Performance & Momentum

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analyze Tesla'\''s price momentum over the past 5 days and compare it against Ford'\''s performance during the same period. Which stock showed stronger relative strength, and what might this indicate about sector rotation dynamics?"}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I'\''m seeing divergence between Apple'\''s price action and its earnings trajectory. Pull the latest earnings data alongside recent price movements and tell me if there'\''s a disconnect between fundamentals and market sentiment."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Compare the volatility profiles of NVDA, AMD, and INTC over their recent trading history. Which semiconductor stock exhibits the most price stability, and how does this correlate with their upcoming earnings calendars?"}'
```

## Earnings & Valuation Analysis

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Microsoft is approaching its earnings announcement. Analyze its recent price behavior leading up to the event and determine whether the market appears to be pricing in a beat, miss, or in-line result based on pre-earnings drift patterns."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Generate a comprehensive analysis comparing Amazon and Meta'\''s earnings surprise history against their post-earnings price reactions. Is there a consistent relationship between EPS beats and subsequent price appreciation?"}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I need to understand whether Netflix'\''s current valuation is justified by its earnings trajectory. Compare its price-to-earnings expansion over the last 5 days against its actual EPS performance and forward estimates."}'
```

## Comparative & Sector Analysis

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Conduct a peer analysis of Walmart, Target, and Costco. Compare their price performance, earnings quality, and upcoming catalyst calendars. Which retailer presents the most compelling risk-reward profile right now?"}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "The semiconductor space has been volatile lately. Pull comprehensive reports for ASML, TSMC, and Qualcomm, then identify which company shows the strongest alignment between its recent earnings performance and market pricing."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Compare the average daily trading volumes and price ranges for Goldman Sachs, Morgan Stanley, and JPMorgan over the past week. Which investment bank is showing the most institutional accumulation patterns?"}'
```

## Temporal & Trend Analysis

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analyze Disney'\''s price trajectory over the last 5 days and calculate its daily returns. Is there evidence of mean reversion, trend continuation, or range-bound behavior? Cross-reference this with their earnings calendar to see if upcoming announcements might be influencing the pattern."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I'\''m researching momentum strategies. Compare the 5-day cumulative returns of Boeing versus Airbus (EADSY), then examine whether the stronger performer also has more favorable upcoming earnings expectations."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Pull Tesla'\''s intraday high-low ranges over the past 5 days and compare them to its longer-term volatility profile. Is the stock exhibiting compression or expansion, and how might this inform an options strategy ahead of earnings?"}'
```

## Risk & Anomaly Detection

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Examine Pfizer'\''s recent trading behavior and flag any days where the closing price deviated significantly from the open-high-low range. Do these anomalies align with any earnings announcements or estimate revisions?"}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I need a risk assessment for holding Meta through their earnings announcement. Show me their historical price behavior in the 5 days leading up to past earnings events, their actual vs. estimated EPS patterns, and the current setup."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Analyze whether Alphabet'\''s current price is trading at a premium or discount to its recent range, and whether this valuation gap is supported by their earnings trajectory and upcoming catalyst calendar."}'
```

## Multi-Factor Integration

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I'\''m building a pairs trade between Coca-Cola and Pepsi. Pull their recent price histories, compare their relative performance, check their upcoming earnings dates, and identify which stock currently offers better entry timing from a catalyst perspective."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Examine the relationship between Visa and Mastercard'\''s price correlation over the past 5 days. Have they been moving in lockstep, or is there divergence? Cross-check their earnings calendars to see if different announcement dates might be creating relative value opportunities."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Generate a comprehensive view of how the mega-cap tech stocks (Apple, Microsoft, Google, Amazon, Meta) have performed relative to each other this week. Which names are showing leadership, and do their earnings calendars suggest this leadership might persist or reverse?"}'
```

## Strategic Decision Support

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I'\''m considering a position in Nvidia ahead of their earnings. Show me their recent price stability or instability, how their current price compares to their recent range, their historical earnings performance (beat/miss patterns), and synthesize whether the risk-reward currently favors taking a position or waiting for post-earnings clarity."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Conduct a tactical analysis of the energy sector by comparing Exxon, Chevron, and ConocoPhillips. I need their recent price momentum, earnings quality metrics, and upcoming catalyst calendars integrated into a single view that identifies which stock offers the best entry point for a 30-day holding period."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I keep hearing about Tesla everywhere. How has it been doing lately compared to Ford? Like, which one has been going up more in the past week or so? Does this mean people are switching from old car companies to electric ones?"}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "My buddy says Apple stock has been weird lately - the price is moving but their actual business numbers look different. Can you check if the stock price makes sense based on how much money they'\''re actually making?"}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I want to buy a chip stock but I hate when prices jump all over the place. Between Nvidia, AMD, and Intel, which one has been the least crazy lately? Also, when are they reporting earnings? I don'\''t want surprises."}'
```

## Earnings & Valuation Analysis

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Microsoft is about to announce their quarterly results soon. Has the stock been going up or down leading into it? Does the price movement suggest people think they'\''ll beat expectations or disappoint?"}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "When Amazon and Facebook report earnings, does beating estimates actually make their stocks go up? Or is it just hype? Show me the pattern - do good earnings actually translate to higher stock prices for these guys?"}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Netflix stock seems expensive. Is the current price justified by how much profit they'\''re actually making? Like, are people overpaying based on the earnings, or is it a fair deal?"}'
```

## Comparative & Sector Analysis

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I shop at Walmart, Target, and Costco. Which one of these stores is the best stock to own right now? Compare how they'\''ve been doing, when they report earnings, and which looks like the safest bet with good upside."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Chip stocks have been all over the place. Look at ASML, Taiwan Semi, and Qualcomm - which company'\''s stock price actually matches up with how well their business is doing? I want the one where the price makes sense."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "My dad worked at a bank. Between Goldman Sachs, Morgan Stanley, and JPMorgan, which one is getting the most buying action from big investors lately? Show me the trading volumes and price swings."}'
```

## Temporal & Trend Analysis

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What'\''s Disney stock been doing this week? Is it bouncing around the same range, trending up, or coming back down after a run? Also check if earnings are coming up - maybe that'\''s why it'\''s moving weird."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I'\''m looking at plane makers - Boeing versus Airbus. Which one has gone up more in the last week? And does the one that'\''s winning also have better earnings expectations? Want to ride the hot hand."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Tesla bounces around a lot every day - big gaps between highs and lows. Is it getting tighter or wider lately? This matters because I'\''m thinking about options before earnings and need to know if it'\''s calming down or getting crazier."}'
```

## Risk & Anomaly Detection

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Check Pfizer for me. Were there any days recently where the closing price was really weird compared to where it opened and traded during the day? If yes, did anything happen - like earnings news or something - that would explain it?"}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Facebook is reporting earnings soon and I'\''m holding shares. How risky is this? Show me what usually happens to the stock before earnings - does it go up, down, or sideways? And do they usually beat or miss their numbers?"}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Is Google stock expensive or cheap right now compared to where it'\''s been trading lately? And does the earnings situation back up whatever the current price is, or is there a mismatch?"}'
```

## Multi-Factor Integration

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Coke versus Pepsi - classic battle. I want to buy one and short the other. Show me how they'\''ve been moving, when earnings are coming, and which one I should buy based on timing. Need the better setup right now."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Visa and Mastercard usually move together since they'\''re in the same business. Have they been moving in sync this week or is one doing better? Check their earnings dates too - maybe different timing creates an opportunity."}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Big tech stocks - Apple, Microsoft, Google, Amazon, Facebook. Which ones are leading the pack this week and which are lagging? Based on when they report earnings, will the winners keep winning or is a rotation coming?"}'
```

## Strategic Decision Support

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I'\''m thinking about buying Nvidia before earnings. Is this smart or dumb? Show me if the stock has been stable or all over the place, how it compares to recent levels, if they usually beat or miss earnings, and give me the bottom line - should I buy now or wait until after they report?"}'
```

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Energy stocks - Exxon, Chevron, ConocoPhillips. I want to hold one for a month. Compare their recent momentum, how good their earnings are, and when they report next. Which one is my best bet for entry right now for a 30-day hold?"}'
```
