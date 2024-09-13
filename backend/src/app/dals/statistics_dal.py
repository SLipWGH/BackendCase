
from sqlalchemy import select, join, func, desc, and_
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession


from app.tables import User, Achievement, UsersAchievements

class StatisticsDAL:
    '''Data Access Layer for operating user info'''

    def __init__(
        self,
        db_session : AsyncSession
    ) -> None:
        self.db_session = db_session

    
    async def get_max_achievements_user(
        self
    )-> User:
        
        query = (
            select(User)
            .join(UsersAchievements, User.id == UsersAchievements.user_id)
            .join(Achievement, UsersAchievements.achievement_name == Achievement.name)
            .group_by(User.id, User.username, User.prefered_language)
            .order_by(func.count(Achievement.name).desc())
            .limit(1) 
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.db_session.execute(query)
        return result.scalar_one()


    async def get_max_achievements_value_sum_user(
        self
    )-> User:
        query = (
            select(User)
            .join(UsersAchievements, User.id == UsersAchievements.user_id)
            .join(Achievement, UsersAchievements.achievement_name == Achievement.name)
            .group_by(User.id, User.username, User.prefered_language)
            .order_by(func.sum(Achievement.value).desc())
            .limit(1) 
        )

        result = await self.db_session.execute(query)
        return result.scalar_one()


    async def users_with_min_achievements_value_difference(
        self
    )-> tuple[User, User]:

        user_scores = (
            select(
                UsersAchievements.user_id,
                func.sum(Achievement.value).label("total_score")
            )
            .join(
                Achievement,
                UsersAchievements.achievement_name == Achievement.name
            )
            .group_by(
                UsersAchievements.user_id
            )
            .cte('UserScores')
        )

        user1_scores = user_scores.alias()
        user2_scores = user_scores.alias()
        user_pairs = (
            select(
                user1_scores.c.user_id.label("user1"),
                user2_scores.c.user_id.label("user2"),
                func.abs(
                    user1_scores.c.total_score - user2_scores.c.total_score
                )
                .label("score_difference")
            )
            .join_from(
                user1_scores,
                user2_scores,
                user1_scores.c.user_id < user2_scores.c.user_id,

            )
            .cte("UserPairs")
        )

        user1 = aliased(User)
        user2 = aliased(User)

        query = (
            select(
                user1,
                user2
            )
            .select_from(
                user_pairs
                .join(user1, user_pairs.c.user1 == user1.id)
                .join(user2, user_pairs.c.user2 == user2.id)
            )
            .order_by(user_pairs.c.score_difference.asc())
            .limit(1)
        )
        # print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.db_session.execute(query)


        return result.fetchone()
 

    async def get_week_achievement_streak_users(
        self
    )-> list[User]:
        
        # Алиасы для таблиц
        users_achievements = aliased(UsersAchievements)
        distinct_days = aliased(users_achievements)
        ranked_days = aliased(distinct_days)
        date_diffs = aliased(ranked_days)
        consecutive_days = aliased(date_diffs)

        # CTE для уникальных дней
        distinct_days_cte = (
            select(
                users_achievements.user_id,
                func.date(users_achievements.date).label('achievement_date')
            )
            .distinct()
            .cte('distinct_days')
        )

        # CTE для ранжирования дней
        ranked_days_cte = (
            select(
                distinct_days_cte.c.user_id,
                distinct_days_cte.c.achievement_date,
                func.row_number().over(
                    partition_by=distinct_days_cte.c.user_id,
                    order_by=distinct_days_cte.c.achievement_date
                ).label('rn')
            )
            .cte('ranked_days')
        )

        # CTE для вычисления разницы
        date_diffs_cte = (
            select(
                ranked_days_cte.c.user_id,
                ranked_days_cte.c.achievement_date,
                (ranked_days_cte.c.rn - func.row_number().over(
                    partition_by=ranked_days_cte.c.user_id,
                    order_by=ranked_days_cte.c.achievement_date
                )).label('gap')
            )
            .cte('date_diffs')
        )

        # CTE для подсчета непрерывных дней
        consecutive_days_cte = (
            select(
                date_diffs_cte.c.user_id,
                func.count().label('consecutive_days')
            )
            .group_by(date_diffs_cte.c.user_id, date_diffs_cte.c.gap)
            .cte('consecutive_days')
        )

        # CTE для выбора пользователей с 7 непрерывными днями
        users_with_7_consecutive_days_cte = (
            select(
                consecutive_days_cte.c.user_id
            )
            .where(consecutive_days_cte.c.consecutive_days >= 7)
            .cte('users_with_7_consecutive_days')
        )

        # Основной запрос
        query = (
            select(
                User.id,
                User.username,
                User.prefered_language
            )
            .select_from(User)
            .join(users_with_7_consecutive_days_cte, User.id == users_with_7_consecutive_days_cte.c.user_id)
        )

        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await self.db_session.execute(query)
        return result.scalars().all()
                

            