CREATE TABLE `celery_log`(
    `retry` VARCHAR(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `status` INT(11) NOT NULL,
    `worker` VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `ctime` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `task_id` VARCHAR(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `msg` TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `info` TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `args` TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `kwargs` TEXT CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
    `id` BIGINT(20) NOT NULL
);
--
-- 資料表索引 `celery_log`
--
ALTER TABLE `celery_log`
  ADD PRIMARY KEY (`id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `celery_log`
--
ALTER TABLE `celery_log`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;