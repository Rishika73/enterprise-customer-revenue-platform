with date_spine as (

    select
        dateadd(
            day,
            row_number() over (order by seq4()) - 1,
            '2025-01-01'::date
        ) as date_day
    from table(generator(rowcount => 1461))

)

select
    date_day,
    year(date_day) as year,
    quarter(date_day) as quarter,
    month(date_day) as month,
    monthname(date_day) as month_name,
    day(date_day) as day_of_month,
    dayofweekiso(date_day) as day_of_week,
    dayname(date_day) as day_name,
    weekofyear(date_day) as week_of_year
from date_spine
