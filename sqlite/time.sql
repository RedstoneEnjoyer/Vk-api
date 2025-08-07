-- Агрегация по времени суток для среднего числа лайков
select
	round(avg(likes), 2) as avg_likes,
	count(*) as post_count,
	case
		when strftime('%H', date) between '04' and '11' then 'morning'
		when strftime('%H', date) between '12' and '16' then 'afternoon'
		when strftime('%H', date) between '17' and '21' then 'evening'
		else 'night'
	end as daytime
from posts
group by daytime
order by likes desc;
