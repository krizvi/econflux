from faker import Faker
import random
from datetime import datetime, timedelta
import os
import argparse

fake = Faker()

# Domain-specific pools
central_banks = [
    "Federal Reserve",
    "European Central Bank",
    "Bank of Japan",
    "Bank of England",
    "Swiss National Bank",
    "Reserve Bank of Australia",
]

policy_actions = [
    {"action": "raise rates by 0.25%", "basis_points": 25, "direction": "hawkish"},
    {"action": "raise rates by 0.50%", "basis_points": 50, "direction": "hawkish"},
    {"action": "cut rates by 0.25%", "basis_points": -25, "direction": "dovish"},
    {"action": "cut rates by 0.50%", "basis_points": -50, "direction": "dovish"},
    {"action": "maintain current rates", "basis_points": 0, "direction": "neutral"},
]

economic_indicators_pool = [
    "GDP growth",
    "Core CPI inflation",
    "headline inflation",
    "unemployment rate",
    "labor force participation",
    "wage growth",
    "retail sales",
    "manufacturing PMI",
    "services PMI",
]

sectors = [
    "banking",
    "insurance",
    "asset management",
    "fintech",
    "broker-dealers",
    "payment processors",
    "credit unions",
]

regulatory_topics = [
    "capital adequacy",
    "liquidity coverage",
    "stress testing",
    "consumer protection",
    "anti-money laundering",
    "cybersecurity",
    "climate risk disclosure",
    "leverage ratios",
]


# Global date tracker to ensure chronological order
class DateTracker:
    def __init__(self, total_records, years_back=3):
        """
        Initialize date tracker with smart spacing based on total records needed.
        
        Args:
            total_records: Total number of records that will be generated
            years_back: How many years in the past to start from
        """
        self.today = datetime.now()
        self.start_date = self.today - timedelta(days=years_back * 365)
        self.last_date = self.start_date
        
        # Calculate available days and average spacing
        total_days_available = (self.today - self.start_date).days
        self.avg_days_between = max(1, total_days_available // total_records)
        
        # Add some randomness bounds (±50% of average)
        self.min_increment = max(1, int(self.avg_days_between * 0.5))
        self.max_increment = max(2, int(self.avg_days_between * 1.5))
        
    def get_next_date(self):
        """Get next chronological date with random increment that won't exceed today"""
        # Calculate how many days we have left until today
        days_until_today = (self.today - self.last_date).days
        
        # If we're getting close to today, use smaller increments
        if days_until_today < self.max_increment:
            increment_days = random.randint(1, max(1, days_until_today))
        else:
            increment_days = random.randint(self.min_increment, self.max_increment)
        
        self.last_date += timedelta(days=increment_days)
        
        # Safety check: never go beyond today
        if self.last_date > self.today:
            self.last_date = self.today
            
        return self.last_date.date()


def generate_monetary_policy_summary(date_tracker):
    bank = random.choice(central_banks)
    policy = random.choice(policy_actions)
    meeting_date = date_tracker.get_next_date()

    # Generate current rate context
    current_rate = round(random.uniform(0.25, 5.5), 2)
    new_rate = round(current_rate + (policy["basis_points"] / 100), 2)

    # Economic justifications
    inflation_rate = round(random.uniform(1.5, 8.5), 1)
    gdp_growth = round(random.uniform(-1.5, 5.5), 1)
    unemployment = round(random.uniform(3.2, 7.8), 1)

    # Construct realistic multi-paragraph summary
    para1 = (
        f"The {bank} concluded its monetary policy meeting on {meeting_date} with the decision to "
        f"{policy['action']}, bringing the policy rate from {current_rate}% to {new_rate}%. "
        f"This {policy['direction']} stance reflects the committee's assessment of current economic conditions, "
        f"particularly the persistent inflation reading of {inflation_rate}% which remains "
        f"{'above' if inflation_rate > 2.5 else 'near'} the central bank's {random.choice([2.0, 2.5])}% target. "
        f"The decision was {'unanimous' if random.random() > 0.3 else 'supported by a majority vote of ' + str(random.randint(7, 12)) + ' to ' + str(random.randint(1, 3))}, "
        f"indicating {'strong consensus' if random.random() > 0.3 else 'some divergence in views'} among policymakers."
    )

    para2 = (
        f"Economic data preceding the meeting showed GDP growth of {gdp_growth}% year-over-year, while "
        f"the unemployment rate held steady at {unemployment}%. Labor market conditions remain "
        f"{'tight' if unemployment < 4.5 else 'balanced'}, with wage growth pressures "
        f"{'contributing to inflation concerns' if inflation_rate > 3 else 'moderating alongside softer demand'}. "
        f"The central bank's statement emphasized that future policy adjustments will be data-dependent, "
        f"contingent upon incoming information about the economic outlook and risks to achieving both "
        f"maximum employment and price stability objectives. Financial market participants had "
        f"{'largely anticipated' if random.random() > 0.4 else 'not fully priced in'} this policy move, "
        f"with fed funds futures suggesting a {random.randint(65, 95)}% probability of this outcome in the week prior."
    )

    para3 = (
        f"Looking ahead, the {bank} signaled that the policy rate path will depend on the evolution of "
        f"economic conditions and their implications for the inflation outlook. "
        f"Committee members' median projection suggests {'additional adjustments may be warranted' if policy['basis_points'] != 0 else 'rates will likely remain stable'} "
        f"over the next {random.randint(6, 18)} months, though significant uncertainty surrounds this baseline forecast. "
        f"Key risks identified include {'geopolitical tensions affecting energy markets' if random.random() > 0.5 else 'potential disruptions to supply chains'}, "
        f"{'tighter global financial conditions' if random.random() > 0.5 else 'slower growth in major trading partners'}, "
        f"and domestic {'labor market dynamics' if random.random() > 0.5 else 'credit conditions'}. "
        f"The central bank reaffirmed its commitment to using all available tools to support the economy "
        f"while maintaining its credibility on inflation control."
    )

    return {
        "bank": bank,
        "date": str(meeting_date),
        "policy_decision": policy["action"],
        "current_rate": current_rate,
        "new_rate": new_rate,
        "direction": policy["direction"],
        "summary": f"{para1}\n\n{para2}\n\n{para3}",
    }


def generate_economic_indicator(date_tracker):
    indicator = random.choice(economic_indicators_pool)
    report_date = date_tracker.get_next_date()

    # Generate contextual values
    current_value = round(random.uniform(-2, 8), 2)
    prior_value = round(current_value + random.uniform(-1.5, 1.5), 2)
    consensus_estimate = round(current_value + random.uniform(-0.5, 0.5), 2)

    para1 = (
        f"The latest {indicator} data released on {report_date} showed a reading of {current_value}%, "
        f"{'exceeding' if current_value > consensus_estimate else 'falling short of'} market consensus expectations of {consensus_estimate}%. "
        f"This represents a {'significant acceleration' if current_value > prior_value + 0.5 else 'moderation' if current_value < prior_value - 0.5 else 'relatively stable trend'} "
        f"compared to the prior period's {prior_value}% figure. "
        f"The {'stronger-than-anticipated' if current_value > consensus_estimate else 'weaker-than-expected'} print "
        f"{'reinforces concerns about' if abs(current_value) > 4 else 'suggests moderate progress toward'} "
        f"{'sustained expansion' if current_value > 2 else 'economic stability'}, prompting analysts to "
        f"{'revise upward their growth forecasts' if current_value > consensus_estimate else 'adopt a more cautious outlook'} "
        f"for the {'coming quarters' if random.random() > 0.5 else 'remainder of the year'}."
    )

    para2 = (
        f"Detailed components of the {indicator} report revealed mixed signals across different sectors. "
        f"The {'services sector showed particular strength' if random.random() > 0.5 else 'manufacturing segment displayed resilience'}, "
        f"contributing approximately {round(random.uniform(0.3, 1.2), 1)} percentage points to the headline figure, "
        f"while {'consumer spending remained robust' if random.random() > 0.5 else 'business investment showed signs of stabilization'}. "
        f"Regional breakdowns indicated {'broad-based improvement' if current_value > prior_value else 'divergent performance'} "
        f"across major metropolitan areas, with {'coastal regions outperforming' if random.random() > 0.5 else 'midwest states showing resilience'}. "
        f"Economists noted that {'seasonal adjustment factors' if random.random() > 0.5 else 'base effects from the prior year'} "
        f"may have {'amplified' if abs(current_value - prior_value) > 1 else 'moderated'} the month-over-month change."
    )

    para3 = (
        f"Market reaction to the {indicator} release was {'swift' if abs(current_value - consensus_estimate) > 0.3 else 'muted'}, "
        f"with {'equity indices advancing' if current_value > consensus_estimate and current_value > 0 else 'bond yields rising'} "
        f"in the immediate aftermath as investors {'recalibrated expectations for central bank policy' if random.random() > 0.5 else 'assessed implications for corporate earnings'}. "
        f"Looking forward, this data point will likely {'factor prominently' if random.random() > 0.5 else 'be carefully considered'} "
        f"in upcoming monetary policy deliberations, particularly given ongoing debates about "
        f"{'the sustainability of current growth trajectories' if current_value > 2 else 'the adequacy of policy support'}. "
        f"Analysts anticipate that subsequent releases will be critical in determining whether this reading represents "
        f"{'a new trend' if abs(current_value - prior_value) > 1 else 'temporary volatility'} or "
        f"{'confirms the establishment of' if random.random() > 0.5 else 'provides further evidence for'} "
        f"a more durable shift in underlying economic conditions."
    )

    return {
        "indicator": indicator,
        "value": current_value,
        "prior_value": prior_value,
        "consensus": consensus_estimate,
        "reported_date": str(report_date),
        "context": f"{para1}\n\n{para2}\n\n{para3}",
    }


def generate_regulatory_changes(date_tracker):
    sector = random.choice(sectors)
    topic = random.choice(regulatory_topics)
    announcement_date = date_tracker.get_next_date()
    effective_date = announcement_date + timedelta(days=random.randint(180, 730))

    # Generate regulatory specifics
    compliance_period = random.randint(12, 36)
    affected_institutions = random.randint(150, 2500)

    para1 = (
        f"Financial regulators announced comprehensive revisions to {topic} requirements for the {sector} sector "
        f"on {announcement_date}, with final rules scheduled to take effect on {effective_date}. "
        f"The new framework represents a significant overhaul of existing standards, impacting approximately "
        f"{affected_institutions} institutions across {'domestic and international operations' if random.random() > 0.5 else 'primarily domestic operations'}. "
        f"Under the updated regime, {'large and mid-sized firms' if random.random() > 0.5 else 'all covered entities'} "
        f"will be required to maintain {topic.split()[0]} levels "
        f"{'at least' if random.random() > 0.5 else 'no less than'} {random.randint(10, 25)}% "
        f"{'above' if random.random() > 0.5 else 'higher than'} current thresholds, reflecting regulators' heightened "
        f"{'concern about systemic risk' if random.random() > 0.5 else 'focus on institutional resilience'}. "
        f"The rulemaking followed {'extensive industry consultation' if random.random() > 0.5 else 'a lengthy comment period'} "
        f"during which {'more than' if random.random() > 0.5 else 'approximately'} {random.randint(150, 450)} "
        f"comment letters were submitted by {'industry participants, consumer advocates, and academic experts' if random.random() > 0.5 else 'stakeholders across the financial services ecosystem'}."
    )

    para2 = (
        f"Key provisions of the final rule include enhanced {'reporting and disclosure obligations' if random.random() > 0.5 else 'monitoring and surveillance requirements'}, "
        f"{'mandatory stress testing scenarios' if 'stress' in topic else 'strengthened governance frameworks'}, "
        f"and {'quarterly attestation requirements' if random.random() > 0.5 else 'annual certification processes'} "
        f"for senior management and board members. Institutions will have {compliance_period} months to achieve full compliance, "
        f"with {'phased implementation milestones' if compliance_period > 18 else 'a single compliance deadline'} "
        f"{'requiring sequential attestation of readiness' if random.random() > 0.5 else 'subject to regulatory examination and validation'}. "
        f"The regulatory impact analysis estimates aggregate implementation costs of "
        f"${random.randint(200, 950)} million across the industry in the first year, "
        f"{'with ongoing annual compliance costs of' if random.random() > 0.5 else 'followed by recurring expenses approximating'} "
        f"${random.randint(75, 300)} million. "
        f"{'Smaller institutions may qualify for simplified requirements' if random.random() > 0.5 else 'Proportionality adjustments will apply based on asset size and risk profile'}, "
        f"though the thresholds for such treatment {'remain subject to supervisory discretion' if random.random() > 0.5 else 'are clearly delineated in the final rule'}."
    )

    para3 = (
        f"Industry response to the regulatory changes has been {'mixed' if random.random() > 0.5 else 'largely critical'}, "
        f"with trade associations {'acknowledging the importance of robust standards while expressing concerns about' if random.random() > 0.5 else 'emphasizing the burden of'} "
        f"implementation timelines and operational complexity. "
        f"{'Major banking groups have indicated they expect to exceed minimum requirements' if random.random() > 0.5 else 'Several institutions have publicly committed to early compliance'}, "
        f"viewing {'strong performance on these metrics as competitive differentiators' if random.random() > 0.5 else 'adherence to enhanced standards as reputational imperatives'}. "
        f"Regulators have committed to {'ongoing dialogue through the implementation period' if random.random() > 0.5 else 'establishing industry working groups to address technical challenges'}, "
        f"including {'quarterly public forums' if random.random() > 0.5 else 'regular roundtable discussions'} "
        f"and {'the publication of supervisory guidance' if random.random() > 0.5 else 'detailed FAQ documents'} "
        f"to address {'emerging interpretive questions' if random.random() > 0.5 else 'common compliance challenges'}. "
        f"The effectiveness of the new framework will be evaluated {'after three years of operation' if random.random() > 0.5 else 'on an ongoing basis'}, "
        f"with potential adjustments based on {'observed outcomes and market developments' if random.random() > 0.5 else 'industry feedback and supervisory experience'}."
    )

    return {
        "sector": sector,
        "topic": topic,
        "announcement_date": str(announcement_date),
        "effective_date": str(effective_date),
        "affected_institutions": affected_institutions,
        "compliance_period_months": compliance_period,
        "summary": f"{para1}\n\n{para2}\n\n{para3}",
    }


def generate_policy_decisions(date_tracker):
    bank = random.choice(central_banks)
    decision_date = date_tracker.get_next_date()
    next_meeting_date = decision_date + timedelta(days=random.randint(42, 60))
    
    # Ensure next meeting doesn't go beyond today
    if next_meeting_date > datetime.now().date():
        next_meeting_date = datetime.now().date() + timedelta(days=random.randint(30, 60))

    policy = random.choice(policy_actions)
    vote_split = (
        f"{random.randint(8, 12)}-{random.randint(0, 3)}"
        if random.random() > 0.3
        else "unanimous"
    )

    # Economic context
    inflation_target = random.choice([2.0, 2.5])
    current_inflation = round(random.uniform(1.2, 6.5), 1)
    core_inflation = round(current_inflation - random.uniform(0.2, 1.5), 1)

    para1 = (
        f"At its policy meeting concluding on {decision_date}, the {bank}'s governing council voted "
        f"{vote_split} to {policy['action']}, marking a {'continuation of' if policy['basis_points'] == 0 else 'shift in'} "
        f"the institution's monetary policy stance. The decision reflects policymakers' assessment that "
        f"{'inflation pressures warrant' if policy['direction'] == 'hawkish' else 'economic conditions justify'} "
        f"{'further policy tightening' if policy['direction'] == 'hawkish' else 'maintaining accommodative conditions' if policy['direction'] == 'dovish' else 'a steady approach'}. "
        f"With headline inflation currently at {current_inflation}% and core inflation at {core_inflation}%, "
        f"{'both measures remain elevated relative to' if current_inflation > inflation_target + 0.5 else 'readings are converging toward'} "
        f"the central bank's {inflation_target}% medium-term objective. "
        f"The accompanying policy statement {'emphasized the committee commitment to' if random.random() > 0.5 else 'reiterated the institution focus on'} "
        f"{'restoring price stability' if current_inflation > inflation_target + 1 else 'supporting sustainable economic expansion'} "
        f"while {'carefully monitoring' if random.random() > 0.5 else 'closely tracking'} "
        f"{'financial stability risks and cross-border spillovers' if random.random() > 0.5 else 'labor market dynamics and credit conditions'}."
    )

    para2 = (
        f"The central bank's updated economic projections, released concurrently with the policy decision, "
        f"{'revised downward' if random.random() > 0.4 else 'maintained'} growth forecasts for the current year to "
        f"{round(random.uniform(0.8, 3.5), 1)}%, while inflation is expected to "
        f"{'decline gradually to' if current_inflation > inflation_target else 'remain near'} "
        f"{round(random.uniform(1.8, 3.2), 1)}% by year-end. "
        f"{'Staff analysis presented to the committee' if random.random() > 0.5 else 'Background materials reviewed by policymakers'} "
        f"highlighted {'persistent tightness in labor markets' if random.random() > 0.5 else 'emerging signs of cooling in consumer demand'}, "
        f"{'elevated household savings rates' if random.random() > 0.5 else 'moderating credit growth'}, "
        f"and {'resilient corporate balance sheets' if random.random() > 0.5 else 'stabilizing business sentiment'}. "
        f"External factors, including {'fluctuations in energy prices' if random.random() > 0.5 else 'supply chain normalization'} "
        f"and {'geopolitical uncertainties' if random.random() > 0.5 else 'global trade dynamics'}, "
        f"were cited as {'key sources of uncertainty' if random.random() > 0.5 else 'important considerations'} "
        f"surrounding the baseline outlook. Several committee members {'expressed concern about' if random.random() > 0.5 else 'noted the potential for'} "
        f"{'second-round effects from wage settlements' if current_inflation > inflation_target else 'disinflationary forces gaining momentum'}."
    )

    para3 = (
        f"Forward guidance contained in the policy statement indicated that "
        f"{'future policy adjustments will depend on' if random.random() > 0.5 else 'the committee will continue to assess'} "
        f"the evolving balance of {'inflation risks and growth prospects' if random.random() > 0.5 else 'economic data and financial conditions'}. "
        f"Market participants interpreted the communication as "
        f"{'signaling a potential pause' if policy['basis_points'] == 0 else 'leaving the door open for additional moves'} "
        f"at the next scheduled meeting on {next_meeting_date}. "
        f"{'Interest rate derivatives pricing' if random.random() > 0.5 else 'Market-implied policy expectations'} "
        f"suggest a {random.randint(35, 85)}% probability of "
        f"{'no change' if random.random() > 0.4 else 'a further ' + str(random.choice([25, 50])) + ' basis point adjustment'} "
        f"at that meeting. The central bank also provided {'updated guidance on balance sheet policy' if random.random() > 0.5 else 'clarification regarding asset purchase operations'}, "
        f"noting that {'quantitative tightening will continue at the current pace' if random.random() > 0.5 else 'the composition of securities holdings may be adjusted'} "
        f"{'absent material changes in financial conditions' if random.random() > 0.5 else 'in line with operational objectives'}. "
        f"{'Governor' if random.random() > 0.5 else 'Chair'} {fake.last_name()}, in post-meeting remarks, "
        f"emphasized that {'the committee remains vigilant and prepared to adjust policy as warranted' if random.random() > 0.5 else 'data dependency remains central to the decision-making framework'}, "
        f"while {'maintaining optionality for future meetings' if random.random() > 0.5 else 'preserving flexibility in the conduct of monetary policy'}."
    )

    return {
        "bank": bank,
        "date": str(decision_date),
        "next_meeting": str(next_meeting_date),
        "policy_decision": policy["action"],
        "vote": vote_split,
        "direction": policy["direction"],
        "current_inflation": current_inflation,
        "core_inflation": core_inflation,
        "inflation_target": inflation_target,
        "summary": f"{para1}\n\n{para2}\n\n{para3}",
    }


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Number of records to generate')
    parser.add_argument('--records', '-r', type=int, default=100, help='Number of records for each dataset')
    parser.add_argument('--years', '-y', type=int, default=3, help='Number of back dated in years')
    args = parser.parse_args()
    TOTAL_RECORDS = args.records  # Change this to 5000 for full dataset
    YEARS_BACK = args.years  # How many years of historical data
    
    # Create output directory
    output_dir = "financial_intelligence_data"
    os.makedirs(output_dir, exist_ok=True)

    # Generate and save datasets
    print("Generating financial intelligence data...\n")
    print(f"Total records per category: {TOTAL_RECORDS}")
    print(f"Date range: {YEARS_BACK} years back to today\n")

    # Monetary Policy Summaries
    print("Generating monetary policy summaries...")
    monetary_date_tracker = DateTracker(TOTAL_RECORDS, YEARS_BACK)
    monetary_policies = []
    for i in range(TOTAL_RECORDS):
        policy = generate_monetary_policy_summary(monetary_date_tracker)
        monetary_policies.append(policy)
    
    with open(f"{output_dir}/monetary_policy_summaries.txt", "w") as f:
        for idx, policy in enumerate(monetary_policies, 1):
            f.write(f"\nMONETARY POLICY REPORT #{idx}\n")
            f.write(f"Institution: {policy['bank']}\n")
            f.write(f"Meeting Date: {policy['date']}\n")
            f.write(f"Policy Action: {policy['policy_decision']}\n")
            f.write(f"Rate Movement: {policy['current_rate']}% → {policy['new_rate']}%\n")
            f.write(f"Policy Stance: {policy['direction'].capitalize()}\n")
            f.write(f"\n{policy['summary']}\n")

    # Economic Indicators
    print("Generating economic indicators...")
    economic_date_tracker = DateTracker(TOTAL_RECORDS, YEARS_BACK)
    economic_data = []
    for i in range(TOTAL_RECORDS):
        indicator = generate_economic_indicator(economic_date_tracker)
        economic_data.append(indicator)
    
    with open(f"{output_dir}/economic_indicators.txt", "w") as f:
        for idx, indicator in enumerate(economic_data, 1):
            f.write(f"\nECONOMIC DATA RELEASE #{idx}\n")
            f.write(f"Indicator: {indicator['indicator']}\n")
            f.write(f"Release Date: {indicator['reported_date']}\n")
            f.write(f"Current Value: {indicator['value']}%\n")
            f.write(f"Prior Value: {indicator['prior_value']}%\n")
            f.write(f"Consensus Forecast: {indicator['consensus']}%\n")
            f.write(f"\n{indicator['context']}\n")

    # Regulatory Changes
    print("Generating regulatory changes...")
    regulatory_date_tracker = DateTracker(TOTAL_RECORDS, YEARS_BACK)
    regulatory_updates = []
    for i in range(TOTAL_RECORDS):
        regulation = generate_regulatory_changes(regulatory_date_tracker)
        regulatory_updates.append(regulation)
    
    with open(f"{output_dir}/regulatory_changes.txt", "w") as f:
        for idx, regulation in enumerate(regulatory_updates, 1):
            f.write(f"\nREGULATORY UPDATE #{idx}\n")
            f.write(f"Affected Sector: {regulation['sector']}\n")
            f.write(f"Regulatory Topic: {regulation['topic']}\n")
            f.write(f"Announcement Date: {regulation['announcement_date']}\n")
            f.write(f"Effective Date: {regulation['effective_date']}\n")
            f.write(f"Affected Institutions: {regulation['affected_institutions']}\n")
            f.write(f"Compliance Period: {regulation['compliance_period_months']} months\n")
            f.write(f"\n{regulation['summary']}\n")

    # Policy Decisions
    print("Generating policy decisions...")
    policy_date_tracker = DateTracker(TOTAL_RECORDS, YEARS_BACK)
    policy_decisions_data = []
    for i in range(TOTAL_RECORDS):
        decision = generate_policy_decisions(policy_date_tracker)
        policy_decisions_data.append(decision)
    
    with open(f"{output_dir}/policy_decisions.txt", "w") as f:
        for idx, decision in enumerate(policy_decisions_data, 1):
            f.write(f"\nPOLICY DECISION ANALYSIS #{idx}\n")
            f.write(f"Central Bank: {decision['bank']}\n")
            f.write(f"Decision Date: {decision['date']}\n")
            f.write(f"Next Meeting: {decision['next_meeting']}\n")
            f.write(f"Policy Action: {decision['policy_decision']}\n")
            f.write(f"Vote Outcome: {decision['vote']}\n")
            f.write(f"Policy Direction: {decision['direction'].capitalize()}\n")
            f.write(f"Current Inflation: {decision['current_inflation']}%\n")
            f.write(f"Core Inflation: {decision['core_inflation']}%\n")
            f.write(f"Inflation Target: {decision['inflation_target']}%\n")
            f.write(f"\n{decision['summary']}\n")

    print("\nDATA GENERATION COMPLETE")
    print(f"\nGenerated {len(monetary_policies)} monetary policy summaries")
    print(f"Generated {len(economic_data)} economic indicators")
    print(f"Generated {len(regulatory_updates)} regulatory updates")
    print(f"Generated {len(policy_decisions_data)} policy decisions")
    print(f"\nAll files saved to: {output_dir}/")
    print("\nFiles created:")
    print(f"  - monetary_policy_summaries.txt")
    print(f"  - economic_indicators.txt")
    print(f"  - regulatory_changes.txt")
    print(f"  - policy_decisions.txt")