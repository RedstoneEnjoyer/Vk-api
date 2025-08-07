-- Агрегация по 
with diff as (
select
    date,
    likes,
    views,
    lag(date) over (order by date) as previous_date,
    round(julianday(date) - julianday(lag(date) over (order by date)), 1) as days_diff
from posts
where date is not null
)
select
	round(avg(likes),2 ) as avg_likes,
    count(*) as post_count,
	case
		when days_diff < 0.5 then "less than 0.5d"
		when days_diff < 1.0 then "between 0.5d 1.0d"
		else "more than 1d"
	end as post_gap
from diff
where days_diff is not null
group by post_gap;
