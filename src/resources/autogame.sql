create table if not exists autogame.game_account
(
    id               varchar(40) not null comment 'ID'
        primary key,
    account_num      int         null comment '账号序号',
    account_type     varchar(40) null comment '账号类型',
    account_name     varchar(40) null comment '账号名称',
    account_password varchar(40) null comment '账号密码',
    role_region      varchar(40) null comment '角色服务器',
    role_name        varchar(40) null comment '角色名称',
    role_class       varchar(40) null comment '角色等级',
    game_package     int         null comment '游戏包名',
    game_acivity     int         null comment '游戏活动名'
)
    comment '游戏账号信息' engine = InnoDB
                           row_format = DYNAMIC;

create table if not exists autogame.game_accounts
(
    id            varchar(40) not null comment '账号组标识'
        primary key,
    accounts_num  int         null comment '账号组序号',
    accounts_name varchar(40) null comment '账号组名称'
)
    comment '账号组信息' engine = InnoDB;

create table if not exists autogame.game_accounts_relation
(
    id           varchar(40) not null comment '账号组关系标识'
        primary key,
    relation_num int         null comment '账号组关系序号',
    acounts_id   varchar(40) null comment '账号组标识',
    account_id   varchar(40) null comment '账号标识'
)
    comment '账号组关系表' engine = InnoDB;

create table if not exists autogame.game_device
(
    id              varchar(40) not null comment '设备ID'
        primary key,
    device_num      int         null comment '设备序号',
    device_serialno varchar(40) null comment '设备序列号',
    device_name     varchar(40) null comment '设备名称',
    device_connect  varchar(40) null comment '设备连接信息'
)
    comment '设备信息表' engine = InnoDB;

create table if not exists autogame.game_god
(
    id         varchar(40) not null comment 'ID'
        primary key,
    god_number int         null comment '式神类型内序号',
    god_name   varchar(40) null comment '式神名称',
    god_type   varchar(40) null comment '式神类型',
    god_sort   int         null comment '式神优先级排序'
)
    engine = InnoDB;

create table if not exists autogame.game_job
(
    id           varchar(40)   not null comment '任务标识'
        primary key,
    device_id    varchar(40)   null comment '设备标识',
    account_ids  varchar(40)   null comment '账号标识组',
    job_num      int           null comment '任务序号',
    week         varchar(20)   null comment '星期',
    start_hour   int           null comment '开始时间',
    end_hour     int           null comment '结束时间',
    projects_id  varchar(40)   null comment '项目组标识',
    project_id   varchar(40)   null comment '项目标识',
    timeout_hour decimal(2, 1) null comment '超时',
    fight_times  int           null comment '战斗次数',
    active_ind   int           null comment '有效标志'
)
    comment '作业' engine = InnoDB;

create table if not exists autogame.game_job_log
(
    id        varchar(40) not null comment '作业日志标识'
        primary key,
    job_date  date        null comment '作业日期',
    job_id    int         null comment '作业标识',
    job_state int         null comment '作业状态'
)
    comment '作业日志' engine = InnoDB;

create table if not exists autogame.game_project
(
    id           varchar(40)  not null comment 'ID'
        primary key,
    project_num  int          null comment '序号',
    project_name varchar(255) null comment '项目名称',
    time_stamp   int          null comment '时间限制标志',
    start_time   int          null comment '开始时间',
    end_time     int          null comment '结束时间',
    remark       varchar(255) null comment '备注'
)
    engine = InnoDB
    row_format = DYNAMIC;

create table if not exists autogame.game_project_log
(
    id          varchar(40)  not null comment 'ID'
        primary key,
    project_id  varchar(40)  null comment '项目ID',
    account_id  varchar(40)  null comment '角色ID',
    device_id   varchar(40)  null comment '设备ID',
    result      varchar(255) null comment '项目执行结果',
    cost_time   bigint       null comment '项目执行耗时（秒）',
    fight_time  int          null comment '项目战斗耗时（秒）',
    fight_times int          null comment '项目战斗次数',
    fight_win   int          null comment '项目战斗胜利次数',
    fight_fail  int          null comment '项目战斗失败次数',
    fight_avg   int          null comment '项目战斗平均用时',
    create_user varchar(40)  null comment '创建人',
    create_time datetime     null comment '创建时间',
    update_user varchar(40)  null comment '修改人',
    update_time datetime     null comment '修改时间'
)
    comment '项目执行结果表' engine = InnoDB;

create table if not exists autogame.game_projects
(
    id            varchar(40)  not null comment 'ID'
        primary key,
    projects_num  int          null comment '序号',
    projects_name varchar(100) null comment '项目名称',
    remark        varchar(255) null comment '备注',
    create_user   varchar(40)  null comment '创建人',
    create_time   datetime     null comment '创建时间',
    update_user   varchar(40)  null comment '修改人',
    update_time   datetime     null comment '修改时间'
)
    comment '游戏项目组' engine = InnoDB
                         row_format = DYNAMIC;

create table if not exists autogame.game_projects_relation
(
    id                varchar(40) not null comment '项目组项目关系ID'
        primary key,
    projects_id       varchar(40) null comment '项目组ID',
    project_id        varchar(40) null comment '项目ID',
    account_id        varchar(40) null comment '账号ID',
    relation_num      int         null comment '关系序号',
    project_num_times int         null comment '项目执行次数',
    wait_before_time  bigint      null comment '项目执行前等待时间',
    wait_after_time   bigint      null comment '项目执行后等待时间',
    project_state     int         null comment '启用状态'
)
    engine = InnoDB
    row_format = DYNAMIC;

