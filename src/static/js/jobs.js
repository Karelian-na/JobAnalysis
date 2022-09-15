layui.use("table", function () {
    var table = layui.table;

    table.render({
        elem: "#jobs",
        url: "/jobs?pageIdx=1&pageSize=30",
        cols: [
            [
                { field: "id", title: "ID", sort: true, align: "center" },
                { field: "name", title: "职位名称", align: "center" },
                { field: "work_area", title: "工作城市", sort: true, align: "center" },
                { field: "experience", title: "经验要求", align: "center" },
                { field: "degree", title: "学历要求", align: "center" },
                { field: "salary_min", title: "最低薪资", sort: true, align: "center" },
                { field: "salary_max", title: "最高薪资", sort: true, align: "center" },
                { field: "company_name", title: "公司名称", align: "center" },
                { field: "type", title: "所属行业", sort: true, align: "center" },
            ],
        ],
        page: true,
        method: "POST",
        request: {
            pageName: "pageIdx",
            limitName: "pageSize"
        },
        toolbar: "default"
    });
});
