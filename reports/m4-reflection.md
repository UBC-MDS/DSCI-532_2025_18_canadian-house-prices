# Reflection on Canadian House Prices Dashboard (Milestone 4)

Since Milestone 3, our team has made substantial progress in enhancing the Canadian House Prices Dashboard. This milestone focuses on the final refinements to the dashboard, addressing ongoing challenges, and ensuring the project aligns with its ultimate goal. Below, we reflect on the implemented features, challenges faced, and the evolution of the project from the initial proposal to the present.

## Implemented Features

In Milestone 4, we focused on refining the user experience and addressing performance and usability issues. Some of the key updates include:

- **Info Button**: We added an **info button** to provide users with additional context about the dashboard, making it easier for first-time users to understand its purpose and functionality.
- **Improved Loading Effect**: To address the performance issues, we refined the loading effect to enhance the user experience during data retrieval. This allows users to be aware of the ongoing loading process, reducing confusion.
- **Alignment and Layout Refinements**: We made minor layout adjustments, such as aligning the sidebar with the bottom of the chart to ensure that everything fits neatly on one page. This creates a more streamlined appearance and improves overall user experience.
- **Handling No Data**: In instances where no data is available, we implemented a message that indicates this, rather than showing empty charts, which could give the wrong impression that the dashboard is broken.
- **Summary Card Update**: We introduced an additional **summary card** to highlight key insights from the data, offering a more concise view of the housing market trends.
- **Color Consistency**: We addressed color inconsistencies, such as matching the province color between the bubble chart and the map to ensure a cohesive visual experience.

## Dealing with Performance Issues

Performance was one of the most significant challenges we faced throughout this project. During Milestone 4, we took several key steps to resolve the performance issues, especially the long loading times that some users experienced when accessing the deployed version of the dashboard on Render. 

### Resolution of Performance Issues:
- **Use of .feather Files**: We resolved the performance issues by switching to **.feather** files for storing location and housing data. These files are faster to load and more efficient for working with large datasets.
- **Updated Data Loading**: We updated the **EDA.ipynb** to extract the locations and housing datasets from the raw data and save them as **.feather files**. Additionally, we modified **data_loader.py** to load these two separate dataframes into the dashboard.
- **Integration with App**: We updated **app.py** to integrate the new **.feather** dataframes and adjusted **charts.py** and **filters.py** to ensure they are using the appropriate dataframes for their functionality.
  
### Optimization Techniques:
- **Refactoring and Computation Improvements**: We focused on optimizing the dashboard's performance through refactoring and computation improvements. 
  - We split callback functions into smaller units for better maintainability and performance.
  - Precomputed **boxplot statistics** for cities and bedrooms during startup to reduce repetitive calculations.
  - We reduced the amount of data sent to Altair by performing more aggregation in Python before passing data to the visualization.

Although the performance was significantly improved, we are continuing to monitor the dashboard for potential further optimizations.

## Differences Compared to Initial Proposal / Sketch

As the project has evolved, it has deviated from the initial proposal and sketch in several areas. While we had originally outlined certain visualization methods, including specific charts and designs, we made deliberate changes to improve user experience, data clarity, and interactivity. Notable differences include:

- **Visualization Methods**: The initial proposal suggested a bar chart for the "Median Price Across Cities," but we ultimately transitioned to a **bubble chart**, which we found to be more engaging and informative for users. Similarly, the use of a **box plot** was eventually replaced by the bubble chart, which proved to be a more dynamic way of displaying data.
- **Map and Chart Changes**: We also replaced the original **Plotly map** with an **Altair map**, which provided clearer projections and a more focused view on Canadian cities. This change was made to enhance usability and make the map more visually coherent with the overall design.
- **Data Representation**: The property type distribution pie chart, initially planned, was removed due to redundancy in the data visualization. We found that it didn’t provide significant added value and decided to simplify the interface instead.

## Evolution of the Dashboard

While the dashboard no longer uses the exact visualizations initially outlined in our proposal, it has evolved into a more functional and user-friendly tool. The various iterations have been a direct response to feedback, usability testing, and performance considerations, which ultimately led to a more refined product.

### Conclusion

The Canadian House Prices Dashboard has evolved significantly from the original proposal. Although it no longer features the exact same visualization methods we initially outlined, we have successfully achieved the ultimate objective of the project: enabling users to compare housing prices across different Canadian cities. The dashboard now provides a clear, interactive, and intuitive platform for users to explore trends in the housing market.

While there are still improvements to be made, particularly in terms of performance, the dashboard has met its core goals. We remain committed to refining the product further and addressing any remaining challenges in future milestones.
