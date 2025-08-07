-- Агрегация по дню недели для среднего числа лайков
select
    round(avg(likes),2 ) as avg_likes,
    count(*) as post_count,
    strftime('%w', date) as weekday
from posts
group by strftime('%w', date)
order by weekday asc;
