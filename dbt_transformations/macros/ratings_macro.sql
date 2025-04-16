{% macro generate_ratings(excellent_score, good_score, average_score, bad_score) %}

{% set rating_tag_1 = 'Excellent' %}
{% set rating_tag_2 = 'Good' %}
{% set rating_tag_3 = 'Average' %}
{% set rating_tag_4 = 'Bad' %}
{% set rating_tag_5 = 'Trash' %}

CASE
  WHEN user_rating >= '{{excellent_score}}' THEN '{{rating_tag_1}}'
  WHEN user_rating >= '{{good_score}}' THEN '{{rating_tag_2}}'
  WHEN user_rating >= '{{average_score}}' THEN '{{rating_tag_3}}'
  WHEN user_rating >= '{{bad_score}}' THEN '{{rating_tag_4}}'
  ELSE '{{rating_tag_5}}'
END AS rating_category

{% endmacro %}