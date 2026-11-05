# Building the Financial Analytics Dashboard in Tableau (Mac)

Tableau runs natively on macOS. This guide delivers everything a Power BI version
would have had: KPI cards, trend, margin, category and department breakdowns,
budget vs actual, cumulative cash flow, slicers, and cross-filtering. It also adds
a variance heatmap, a metric-selector parameter and a month-over-month growth view.

Estimated time: 2 to 3 hours for a first build.

---

## STEP 0: Pick your Tableau edition (decides how you connect to data)

| Edition | Cost | Connects to MySQL? | How to get it |
|---|---|---|---|
| **Tableau Desktop Public Edition** (this is what the *Tableau for Students* offer currently gives you; it is also free for anyone) | Free, no renewal | **No.** Files only (CSV / Excel) | tableau.com student page → **Get Tableau for Free** → create a free Tableau Public profile → download |
| **Tableau Desktop** (full version) | 14-day free trial | **Yes, live connection** | tableau.com/products/trial |

**Recommended path:** build the whole dashboard in **Public Edition using the CSVs** in
`tableau_setup/data/` (Step 1, Path B). It is free with no expiry, and it gives you a public
link for your resume. State in your README that the CSVs are exports of the MySQL views.

Use the 14-day trial only if you also want a live MySQL connection screenshot. If you do,
finish the MySQL setup first so you can connect and capture it within the 14 days.

> Public Edition publishes workbooks to the public web and is not for commercial use
> (internship or job work). Neither matters for a portfolio project on synthetic data.
> The student offer does not include Tableau Cloud or Tableau Prep.

---

## STEP 1: Connect to the data

### Path A: Full Tableau Desktop (14-day trial) to MySQL (live)
1. Make sure MySQL is running and you completed `SETUP_GUIDE.md` Parts 1 to 4, then run
   `mysql_setup/05_tableau_views.sql` in Workbench to create the two views.
2. Open Tableau Desktop → left panel **Connect → To a Server → MySQL**.
3. Tableau shows a driver download link if the MySQL driver is missing. Install the driver
   from that link, then **quit and reopen Tableau**.
4. Enter: Server `localhost`, Port `3306`, Username `root`, your password → **Sign In**.
5. Database dropdown → `finance_dashboard`.
6. Drag **`vw_transactions`** onto the canvas. Then drag **`vw_budget_vs_actual`** next to it.
7. Tableau draws a line between them (a *relationship*, not a join). Edit it so it uses
   **three** matching fields, all set with `=`:
   - `Date` = `Date`
   - `Department` = `Department`
   - `Type` = `Type`
8. Leave the connection as **Live**. Click **Sheet 1** at the bottom.

### Path B: Public Edition (or any edition) with CSV files  <- recommended
1. **Connect → Text file** → choose `tableau_setup/data/transactions.csv`.
2. Drag `budget_vs_actual.csv` onto the canvas next to it (use **Add** under Files).
3. Edit the relationship exactly as in Path A step 7 (Date, Department, Type).
4. Click **Sheet 1**.

### Why three fields in the relationship? (interview talking point)
Budget exists once per **month × department × type**. Transactions exist many times per
month. Relating on department alone would repeat each budget figure for every
transaction row and inflate budget totals. Relating on all three fields, with Tableau
relationships (which aggregate each table at its own level of detail), keeps both
totals correct. The files have been reconciled: actuals total ₹13,702,815.91 in
both the transaction data and the budget-vs-actual data.

### Data type check (do this once)
In the Data pane, click the small icon next to each field:
- `Date` → **Date**
- `Amount`, `Actual Amount`, `Budgeted Amount`, `Variance` → **Number (decimal)**
- `Department`, `Type`, `Category` → **String**

---

## STEP 2: Create calculated fields

Right-click in the Data pane (empty area) → **Create Calculated Field**. Name each field
exactly as shown, paste the formula, click OK.

```
Total Revenue
SUM(IF [Type] = "Revenue" THEN [Amount] END)

Total Expense
SUM(IF [Type] = "Expense" THEN [Amount] END)

Net Profit
[Total Revenue] - [Total Expense]

Profit Margin %
IF [Total Revenue] = 0 THEN NULL ELSE [Net Profit] / [Total Revenue] END
```

For budget vs actual (these use the budget table's fields):

```
Actual Expense
SUM(IF [Type] = "Expense" THEN [Actual Amount] END)

Budgeted Expense
SUM(IF [Type] = "Expense" THEN [Budgeted Amount] END)

Expense Variance
[Actual Expense] - [Budgeted Expense]

Expense Variance %
IF [Budgeted Expense] = 0 THEN NULL ELSE [Expense Variance] / [Budgeted Expense] END

Budget Status
IF [Expense Variance] > 0 THEN "Over Budget" ELSE "Within Budget" END
```

For trends:

```
Cumulative Cash Flow
RUNNING_SUM([Net Profit])

Revenue MoM Growth %
(ZN([Total Revenue]) - LOOKUP(ZN([Total Revenue]), -1)) / ABS(LOOKUP(ZN([Total Revenue]), -1))
```

> HR has a ₹0 revenue budget, so any ratio against it would divide by zero. The
> `IF … = 0 THEN NULL` guards above prevent errors.

Format the fields once so every sheet inherits it: right-click the field → **Default
Properties → Number Format**
- Total Revenue, Total Expense, Net Profit, Actual/Budgeted Expense, Expense Variance, Cumulative Cash Flow → **Currency (Custom)** with symbol `₹`, 0 decimals
- Profit Margin %, Expense Variance %, Revenue MoM Growth % → **Percentage**, 1 decimal

---

## STEP 3: Build the sheets

Create each sheet with the **New Worksheet** icon at the bottom and rename it by
double-clicking its tab. Drag fields from the Data pane onto Columns, Rows, Marks.

### Sheet 1: `KPI Revenue`, `KPI Expense`, `KPI Profit`, `KPI Margin`
Four small sheets, one per KPI.
1. Drag the measure (e.g. `Total Revenue`) onto **Text** in the Marks card.
2. Click **Text** → click `…` → make the number large (28 to 32 pt, bold).
3. Hide the headers (right-click → uncheck Show Header) and set **Fit → Entire View**.
4. Colour each: Revenue blue, Expense red, Profit green, Margin gold.

### Sheet 2: `Trend` (Revenue vs Expense vs Profit by month)
1. Columns: `Date` → right-click the pill → choose **Month** (the *continuous* one, the green pill with exact date).
2. Rows: drag `Total Revenue`, then drag `Total Expense` and drop it on the same axis; add `Net Profit` the same way.
3. If Tableau creates a *Measure Names* legend, that is fine. Set colours: Revenue blue, Expense red, Net Profit green (right-click legend → Edit Colors).
4. Marks: **Line**, add **Circle** for each point via the Marks card dropdown.
5. Title: `Revenue, Expense and Net Profit by Month`.

### Sheet 3: `Margin Trend`
1. Columns: `Date` (Month, continuous). Rows: `Profit Margin %`.
2. Right-click the axis → **Add Reference Line** → Per Pane → Average → label *Average*.
3. Colour gold. Title: `Profit Margin % Over Time`.

### Sheet 4: `Expense by Category`
1. Rows: `Category`. Columns: `Total Expense`.
2. Drag `Type` to **Filters** → tick only **Expense**. (Total Expense already filters by type; this keeps categories that exist only for revenue out of the list.)
3. Sort descending (click the sort icon on the axis).
4. Marks: Bar, label showing value (Marks → Label → Show mark labels).
5. Add a tooltip showing `% of Total`: Marks → Tooltip → insert `<Total Expense>`; and for the share, drag `Total Expense` to **Detail**, right-click it → **Quick Table Calculation → Percent of Total**.

### Sheet 5: `Revenue by Department`
1. Rows: `Department`. Columns: `Total Revenue`. Sort descending.
2. A bar chart is more readable than a donut for 6 categories; use it. (If you want a donut for variety: Marks → Pie, drag `Department` to Color, `Total Revenue` to Angle.)
3. Title: `Total Revenue by Department`.

### Sheet 6: `Budget vs Actual`
1. Columns: `Department`. Rows: `Actual Expense` and `Budgeted Expense` (drop the second on the same axis → right-click → **Dual Axis**, **Synchronize Axis**).
2. Marks: Actual → Bar (red), Budgeted → Line with circle (blue).
3. Or simpler and clearer: Rows `Department`, Columns `Expense Variance %`, colour by `Budget Status` (Over = red, Within = green).
4. Filter: drag `Date` to Filters → **Months** → pick the latest month, or show a quick filter (see Step 5).

### Sheet 7: `Cash Flow`
1. Columns: `Date` (Month, continuous). Rows: `Cumulative Cash Flow`.
2. Marks: **Area**. Colour teal. Title: `Cumulative Cash Flow`.

### Sheet 8 (bonus): `Variance Heatmap`
1. Rows: `Department`. Columns: `Date` (Month, discrete).
2. Marks: **Square**, `Expense Variance %` onto **Color** and **Label**.
3. Edit colours: diverging (green for under budget, red for over budget), centre 0.
This single view shows *which department overspent in which month*, and it is the
view most recruiters remember.

### Sheet 9 (bonus): `MoM Growth`
1. Columns: `Date` (Month, continuous). Rows: `Revenue MoM Growth %`.
2. Marks: **Bar**. Colour: right-click the field on Color → positive green, negative red (Edit Colors → Stepped Color / Diverging, centre 0).
3. The first month shows blank (nothing to compare to); that is expected.
Place it beside `Cash Flow` on the dashboard if there is room.

---

## STEP 4: Add parameters (makes it interactive like Power BI field parameters)

### Parameter 1: `Select Metric`
1. Data pane → small arrow → **Create Parameter**.
2. Name `Select Metric`, Data type **String**, Allowable values **List**:
   `Revenue`, `Expense`, `Net Profit`.
3. Create calculated field `Selected Metric`:
```
CASE [Select Metric]
WHEN "Revenue" THEN [Total Revenue]
WHEN "Expense" THEN [Total Expense]
WHEN "Net Profit" THEN [Net Profit]
END
```
4. Use `Selected Metric` on Sheet 2/5 instead of a fixed measure. Right-click the parameter → **Show Parameter**, and viewers can switch the metric.

### Parameter 2: `Top N Categories`
Integer, range 3 to 8, default 5. Drag `Category` to Filters → **Top** tab → By field → Top `[Top N Categories]` by `Total Expense`.

---

## STEP 5: Filters (the "slicers")

On any sheet: drag the field to **Filters**, then right-click the filter pill → **Show Filter**.
- `Date` → **Range of dates** (slider)
- `Department` → **Multiple Values (dropdown)**
- `Type` is not needed as a filter because the measures already handle it.

To make a filter apply to all sheets: right-click the filter on the shelf → **Apply to Worksheets → All Using This Data Source**.

---

## STEP 6: Assemble the dashboard

1. Click **New Dashboard** (icon next to New Worksheet). Name it `Financial Analytics Dashboard`.
2. Size (bottom left) → **Fixed size → Desktop (1366 × 768)** or *Automatic* if you want it to resize.
3. Layout order (use *Horizontal* and *Vertical* containers from the Objects list so it stays aligned):

```
┌───────────────────────────────────────────────────────────────┐
│ Title: Financial Analytics Dashboard                  [filters]│
├──────────┬──────────┬──────────┬──────────────────────────────┤
│ KPI Rev  │ KPI Exp  │ KPI Prof │ KPI Margin                   │
├──────────┴──────────┴──────────┼──────────────────────────────┤
│ Trend (wide)                   │ Margin Trend                 │
├────────────────┬───────────────┼──────────────────────────────┤
│ Expense by Cat │ Rev by Dept   │ Budget vs Actual             │
├────────────────┴───────────────┴──────────────────────────────┤
│ Variance Heatmap  │  Cash Flow                                 │
└───────────────────────────────────────────────────────────────┘
```
4. Drag the sheets in from the left list. Set each to **Fit → Entire View**.
5. Add a **Text** object at the bottom with your one-line insight (see below).
6. Colour the dashboard background (Dashboard → Format) a light grey or dark navy; keep text readable.

### Make it interactive (Actions)
**Dashboard → Actions → Add Action → Filter**
- Source: `Revenue by Department`; Target: all other sheets; Run on **Select**; Clearing selection → **Show all values**.
Now clicking a department bar filters the entire dashboard, which is the "cross-filtering" behaviour people expect from Power BI.

Add a **Highlight** action too: Source `Expense by Category` → Target `Trend` on Hover.

### Tooltips
Edit each sheet's **Tooltip** (Marks card) so hovering shows plain English, for example:
`<Department>: spent <Actual Expense> vs budget <Budgeted Expense> (<Expense Variance %>)`.

---

## STEP 7: Write one concrete insight on the dashboard

Use real numbers from your own dashboard. Based on the reconciled data:
- Total revenue ₹73.65 lakh, expense ₹63.38 lakh, net profit ₹10.27 lakh (13.9% margin).
- Monthly revenue rose from about ₹2.72 lakh to ₹3.67 lakh over 24 months (+34.7%).
- Every department exceeded its expense budget in 10 to 15 of the 24 months (Operations 15, IT/Marketing/R&D 13, HR 11, Sales 10). R&D has the largest overspend (3.5%). That is a systematic budgeting gap, not a one-off.

Put a version of that in the Text box, and a recommendation: *"Re-baseline department
budgets to actual cost growth (about 1.2% a month vs about 0.9% assumed), starting with R&D and Operations."*

---

## STEP 8: Save, publish, screenshot

- **Tableau Desktop:** File → Save As → `Financial_Analytics_Dashboard.twbx` (the **.twbx** packages the data; **.twb** does not). Export an image: Dashboard → Export Image.
- **Tableau Public:** File → Save to Tableau Public → sign in → it opens in your browser; copy the URL for your resume and README.
- Take 3 screenshots (full dashboard, heatmap, budget vs actual) and put them in `screenshots/`.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| MySQL option missing in Tableau Public | Expected; Public only reads files. Use the CSVs. |
| Driver message when connecting to MySQL | Use the link in the dialog, install, restart Tableau. |
| Totals look too big | Relationship must use all three fields (Date, Department, Type). |
| Date shows as text | Click the field's icon in Data pane → Date. |
| Budget shows ₹0 for Revenue in HR | Correct; HR has no revenue budget. |
| Red "!" on a calculated field | Field names must match exactly (check capitalisation and that `Type` values are `"Revenue"` / `"Expense"`). |
| Can't connect to MySQL | Start MySQL: System Settings → MySQL → Start MySQL Server. |

---

## How this maps to your resume line

> *Power BI / Tableau: dashboard creation and visualization*

You can truthfully say (once you have built it): **built an interactive Tableau dashboard (KPIs, trends, budget-variance heatmap) on a MySQL data source, with parameter-driven metrics and cross-filter actions.**
