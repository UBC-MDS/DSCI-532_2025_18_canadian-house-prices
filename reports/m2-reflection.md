# Reflection on Dashboard Implementation

This reflection compares our **Milestone 1 Proposal** ([m1_proposal.md](https://github.com/UBC-MDS/DSCI-532_2025_18_canadian-house-prices/blob/feature/update-readme-milestone2/reports/m1_proposal.md)) with our current **Milestone 2 Dashboard**. We discuss which features were successfully implemented, which were not, and the reasons for any deviations or improvements.

---

## 1. Implemented Features

1. **Map Visualization**  
   - **Proposal:** We planned to display a map of Canada highlighting the average house prices in different cities.  
   - **Implementation:** In the current dashboard, we used a choropleth-style (or marker-based) map to show house price distribution across the top 45 cities. This meets the original goal of providing a geographical overview.

2. **Filters for City and Bedrooms/Bathrooms**  
   - **Proposal:** We aimed to allow users to filter data by city and number of bedrooms/bathrooms.  
   - **Implementation:** Our dashboard includes sidebar filters for city, province, number of bedrooms, and bathrooms. Users can apply these filters interactively, which matches our original plan and enhances the user experience.

3. **Box Plot for Price Distributions**  
   - **Proposal:** We initially planned a scatter plot for price vs. number of bedrooms/bathrooms.  
   - **Implementation:** After experimenting, we opted for a **box plot** to better display the range and outliers. This small pivot aligns with our original intent—showing how bedrooms/bathrooms relate to price—but presents the data more clearly.

---

## 2. Partially Implemented or Deferred Features

1. **Forecasting or Predictive Modeling**  
   - **Proposal:** We mentioned exploring a simple predictive model for future house prices.  
   - **Current Status:** Due to time constraints, we have not yet implemented forecasting. We plan to integrate this feature in a future milestone once we finalize our data sources and refine our approach.

2. **Detailed Provincial Comparisons**  
   - **Proposal:** We planned to show additional provincial-level metrics (e.g., average lot size, historical trends).  
   - **Current Status:** We partially implemented a provincial filter, but we have not included deeper historical data. We’re aiming to incorporate more advanced provincial comparisons in future iterations.

---

## 3. Changes from the Original Plan

1. **Box Plot Instead of Scatter Plot**  
   - **Reason:** Box plots highlight median, quartiles, and outliers more effectively, making it easier to compare distributions across multiple cities or bedroom categories.

2. **Added an “Average Bedrooms” Display**  
   - **Reason:** Based on peer feedback, we added a numeric summary (e.g., “Average Bedrooms: 2.7”) to the top of the dashboard. This quick reference helps users gauge the typical property size at a glance.

3. **Refined Aesthetics**  
   - **Reason:** We changed some color schemes and layout choices after testing user interactions, ensuring the dashboard is more readable and visually appealing.

---

## 4. Rationale and Effectiveness

- **Why These Changes Improve the Dashboard:**  
  - A box plot offers a clearer, more intuitive snapshot of price distribution and outliers across different cities or bedroom counts.  
  - Adding a real-time numerical summary (like average bedrooms) immediately gives users contextual insights.  
  - The improved layout and color scheme ensure better readability and user engagement.

- **Trade-Offs:**  
  - We postponed forecasting because we wanted to focus on refining core visualizations.  
  - Advanced historical or provincial comparisons are on hold until we gather more complete datasets.

---

## 5. Future Directions

- **Implement Forecasting:**  
  We plan to integrate a simple linear or time-series model to predict future price trends.
- **Expand Filters and Data Sources:**  
  We aim to include more features (e.g., property type, property age) and deeper historical data.
- **Refine UI/UX:**  
  We’ll continue to gather feedback to enhance navigation, filter responsiveness, and overall user flow.

---

## Conclusion

Our Milestone 2 dashboard closely aligns with the **Milestone 1 Proposal** in terms of the core features—map-based visualization, interactive filters, and comparative plots. We made a few strategic adjustments to improve clarity (using box plots) and usability (displaying average bedrooms). While some features (like forecasting) remain on our roadmap, the current dashboard fulfills the main objectives of our original proposal and sets a solid foundation for further development.