# Reflection on Dashboard Implementation

This reflection compares our **Milestone 1 Proposal** ([m1_proposal.md](https://github.com/UBC-MDS/DSCI-532_2025_18_canadian-house-prices/blob/feature/update-readme-milestone2/reports/m1_proposal.md)) with our current **Milestone 3 Dashboard**. We discuss which features were successfully implemented, which were not, and the reasons for any deviations or improvements.

---

# Best Practices and Deviation

The dashboard is designed with data visualization best practices in mind. While some of the choices, like the interactive bubble chart, deviate from traditional static charts, they add a more engaging and informative experience for the user. The use of interactive elements throughout the dashboard ensures that users can manipulate the data to their preferences and discover trends.

## Intentional Design Deviations

We’ve made intentional deviations from certain design elements to enhance the user experience:

- **Removing the Top Bar**: We decided to remove the top bar and include the title within the sidebar to maximize screen space and ensure a cleaner layout.
- **Rearranging Elements**: The province dropdown has been moved above the city dropdown for improved user flow, and we’re experimenting with text formatting, such as making the font on cards lighter to improve readability.

# Changes from the Initial Proposal

Several aspects of the dashboard have deviated from the initial design for improved usability:

- **Replacement of the Bar Chart**: The bar chart, which compared median prices across cities, was replaced with a box plot (positioned at the top-right) due to redundancy—both charts displayed similar information, but the box plot offers more comprehensive insights into price distribution.
- **Map Filtering**: The map now filters data to only show Canadian cities, in line with the project’s scope. We also changed the map projection to the default one for Canada for better clarity and accuracy.

# Known Issues and Limitations

There are a few areas of the dashboard that still need refinement:

- **Price Distribution**: The box plot could benefit from sorting by the median price to offer users a more intuitive view of the data, rather than just relying on city order.
- **Zero Bedrooms/Bathrooms**: This refers to studio apartments.
- **Geospatial Data**: The map's tooltip has been simplified by removing the latitude/longitude values. However, we want to enhance the map by marking all cities when nothing is selected, providing a better overall view for the user.
- **Card Backgrounds**: We are experimenting with adding background colors to the cards displaying key statistics (e.g., average number of bedrooms), along with using light text for better contrast and readability.

## Conclusion

In conclusion, the dashboard has been intentionally designed with best practices in data visualization to provide users with an engaging, interactive experience. While some design choices deviate from traditional approaches, such as the use of interactive elements and the removal of the top bar, these adjustments have been made to enhance usability and optimize screen space. Changes from the initial proposal, including the substitution of the bar chart with a box plot and the refinement of map filtering, demonstrate a commitment to improving clarity and providing deeper insights. Despite a few known limitations, such as the need for further refinement in price distribution and map features, the dashboard continues to evolve with the user experience in mind. Moving forward, further adjustments will ensure a more intuitive and informative interface, allowing users to explore the data more effectively.