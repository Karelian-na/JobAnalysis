var form = document.querySelector("form");
var renderer = null;
// var form = document.querySelector("form");
// var formData = new FormData(form);
// var renderer = null;
// form.onsubmit = function () {
//     $.ajax({
//         method: "POST",
//         url: "/jobs",
//         data: $(form).serialize(),
//         // data: formData,
//         processData: false,  // 不处理数据
//         contentType: false,
//         success: (result) => {
//             const data = JSON.parse(result);
//             renderer.reload({
//                 data: data
//             });
//         },
//     });
//     return false;
// }



layui.use(["table", "form", "layer"], function () {
    var table = layui.table;
    var form = layui.form;
    var layer = layui.layer;
    var $ = layui.jquery;

    renderer = table.render({
        elem: "#jobs",
        url: "/jobs?pageIdx=1&pageSize=30",
        cols: [
            [
                { field: "number", type: "numbers", title: "序号", align: "center" },
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
        limit: 20,
        page: true,
        method: "POST",
        request: {
            pageName: "pageIdx",
            limitName: "pageSize"
        },
        toolbar: "default",
        height: "full-100"
    });
});
form.onsubmit = () => {
    layui.table.reload('jobs', {
        page: {
            curr: 1 //重新从第 1 页开始
        },
        where: {
            search_field: form["search_field"].value,
            search_content: form["search_content"].value
        }
    });
    return false;
}