# Capital One Airbnb Challenge 2017 #  
  
[Heroku Link](https://guarded-tor-54790.herokuapp.com/)  
  
### Goals ###  
1. **Visualize three trends in San Francisco Airbnb data over one year**  
    1. I decided to analyze the total number of listings per neighborhood in San Francisco, the average review score (out of 100) for listings per neighborhood in San Francisco, and the total number of available days of listings per neighborhood in San Francisco.  
2. **Given geolocation of a property, estimate the weekly average income you can make with Airbnb**  
    1. Based on data over 365 days, I decided to take the average of the weekly income values for Airbnb properties 0.01 degrees of latitude and 0.01 degrees of longitude within the given geolocation.  
3. **Given geolocation of a property, determine ideal price per night to optimize Airbnb bookings revenue**  
    1. Based on data over 365 days, I decided to account for three factors (geolocation, number of bedrooms, and number of bathrooms) when determining the ideal price. I chose to incorporate data about the number of bedrooms and number of bathrooms in my analysis to increase the accuracy of the recommended optimal price per night. For this analysis, I also took the average of income values for Airbnb properties 0.01 degrees of latitude and 0.01 degrees of longitude within the given geolocation.  
    2. Furthermore, in the HTML form for optimizing price, users can choose how many days of data to use when determining the optimal price. Users have options of the past 30 days, the past 60 days, the past 90 days, or the past 365 days.  
4. **Determine the San Francisco neighborhood that averages the most positive reviews**  
    1. Examining the second visualized trend, we can determine the neighborhood with the highest average for review scores.
  
### Design ###  
1. **Back-End**  
    1. Using Python and Flask, I built a web application to analyze and display San Francisco Airbnb data over one year subsequently deployed the web application using Heroku.  
    2. Specifically, I utilized the pandas library for analyzing the data contained in .csv files, the matplotlib library to visual three trends in the data, and the numpy library for configuring graph axes. I also used a BytesIO object to keep track of the binary data of each graph so that I could convert them to PNG images, and base64 encoding was used to convert the graphs as PNG images into a form that could be passed into and displayed in HTML.  
  
2. **Front-End**  
    1. Using HTML and CSS with the Bootstrap library, I designed the pages to display data and forms to take user input for the web application. Jinja was used to access Python variables in HTML.  
