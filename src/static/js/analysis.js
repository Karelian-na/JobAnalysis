document.addEventListener("DOMContentLoaded", () => {
    var data = null;
    var tableRenderer;
    var first = true;
    const salaryBarChart = echarts.init(document.getElementById("salaryBar"));
    const groupPieChart = echarts.init(document.getElementById("groupPie"));

    const degreePieChart = echarts.init(document.getElementById("degreePie"));
    const degreeBarChart = echarts.init(document.getElementById("degreeBar"));

    const experiencePieChart = echarts.init(document.getElementById("experiencePie"));
    const experienceBarChart = echarts.init(document.getElementById("experienceBar"));

    const form = document.querySelector("form");

    form.onsubmit = () => {
        $.ajax({
            method: "POST",
            data: $(form).serialize(),
            url: `/analysis/${window.location.href.substring(window.location.href.lastIndexOf("/") + 1)}`,
            beforeSend: function () {
                index_wait = layer.load(0, {  //发送请求前调用load方法
                    shade: [0.5, '#fff'],  //0.5透明度的白色背景
                });
            },
            complete: function () {  //load默认不会关闭，请求完成需要在complete回调中关闭
                layer.close(index_wait);
            },
            success: (result) => {
                data = JSON.parse(result);
                renderSalaryBarChart(data);
                renderGroupPieChart(data);
                renderDegreePieChart(data);
                renderDegreeBarChart(data);
                renderExperiencePieChart(data);
                renderExperienceBarChart(data);
                renderGroupTable(data);
            },
            error: (_xhr, _status, _error) => {
                window.alert(_error);
            },
        });
        return false;
    };

    function renderSalaryBarChart(data) {
        salaryBarChart.clear();
        const salaryData = data["salaryProportion"];
        salaryBarChart.clear();
        salaryBarChart.setOption({
            title: {
                text: `前 ${Object.keys(salaryData).length} 职业薪水对比图`,
                left: "center",
            },
            xAxis: {
                type: "category",
                data: Object.keys(salaryData),
                axisLabel: {
                    color: 'black',
                    interval: 0,
                    route: 30
                    // formatter: function (value) {
                    //     const str = value.split('');
                    //     return str.join('\n');
                    // }
                },
            },
            yAxis: {
                type: "value",
            },
            grid: {
                left: "3%",
                right: "4%",
                bottom: "3%",
                containLabel: true,
            },
            series: [
                {
                    name: "最低工资",
                    type: "bar",
                    stack: "salary",
                    emphasis: {
                        focus: "series",
                    },
                    data: Object.values(salaryData).map((value) => value.min),
                },
                {
                    name: "波动范围",
                    type: "bar",
                    stack: "salary",
                    emphasis: {
                        focus: "series",
                    },
                    data: Object.values(salaryData).map((value) => value.max - value.min),
                },
                {
                    name: "平均薪资",
                    type: "line",
                    emphasis: {
                        focus: "series",
                    },
                    data: Object.values(salaryData).map((value) => value.mid),
                },
            ],
        });

    }

    // 热门职业分析
    function renderGroupPieChart(data) {
        groupPieChart.clear();
        const groupData = data["groupProportion"];
        groupPieChart.clear();
        groupPieChart.setOption({
            title: {
                text: `前 ${Object.keys(groupData).length} 职业权重图`,
                left: "center",
            },
            legend: {
                top: "bottom",
            },
            toolbox: {
                show: true,
                feature: {
                    mark: { show: true },
                    dataView: { show: true, readOnly: false },
                    restore: { show: true },
                    saveAsImage: { show: true },
                },
            },
            series: [
                {
                    name: "Nightingale Chart",
                    type: "pie",
                    radius: [50, 100],
                    center: ["50%", "45%"],
                    roseType: "area",
                    itemStyle: {
                        borderRadius: 8,
                    },
                    data: Object.keys(groupData).map((key) => {
                        return {
                            name: key,
                            value: groupData[key],
                        };
                    }),
                },
            ],
        });
    }

    function renderGroupTable(data) {
        const datas = Object.keys(data["groupProportion"]).map((value) => {
            const salary = data["salaryProportion"][value];
            return {
                name: value,
                averageSalary: `${salary["min"]}k-${salary["max"]}k`,
                amount: data["groupProportion"][value],
            };
        });
        if (first) {
            layui.use("table", () => {
                var table = layui.table;
                tableRenderer = table.render({
                    elem: "#groupTable",
                    title: `前${datas.length}职业详细信息`,
                    cols: [
                        [
                            { field: "serial", type: "numbers", title: "排名", align: "center", width: "24%" },
                            { field: "name", title: "职业名称", align: "center", width: "24%" },
                            { field: "averageSalary", title: "平均薪资范围", sort: true, align: "center", width: "25%" },
                            { field: "amount", title: "招聘公司数目", sort: true, align: "center", width: "25%" },
                        ],
                    ],
                    data: datas,
                    initSort: {
                        field: "amount",
                        type: "desc",
                    },
                });
                first = false;
            });

        } else {
            tableRenderer.config.limit = datas.length;
            tableRenderer.reload({
                data: datas,
            });
        }
        document.getElementById("groupTable").closest(".table").previousElementSibling.innerText = `前 ${datas.length} 职业详细信息`
    }
    // 热门职业分析结束

    // 学历分析
    function renderDegreePieChart(data) {
        degreePieChart.clear();
        const degreeData = data["degreeProportion"];
        degreePieChart.setOption({
            title: {
                text: `所有职业所需学历占比`,
                left: "center",
            },
            legend: {
                top: "bottom",
            },
            tooltip: {
                trigger: "item",
            },
            series: [
                {
                    name: "Access From",
                    type: "pie",
                    radius: ["40%", "70%"],
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: "#fff",
                        borderWidth: 2,
                    },
                    label: {
                        show: false,
                        position: "center",
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: "40",
                            fontWeight: "bold",
                        },
                    },
                    labelLine: {
                        show: false,
                    },
                    data: Object.keys(degreeData).map((key) => {
                        return {
                            name: key,
                            value: degreeData[key],
                        };
                    }),
                },
            ],
        });
    }

    function renderDegreeBarChart(data) {
        degreeBarChart.clear();
        const categoryDegreeData = data["categoryDegreeProportion"];
        const categories = Object.keys(categoryDegreeData);
        degreeBarChart.setOption({
            tooltip: {
                trigger: "axis",
                axisPointer: {
                    // Use axis to trigger tooltip
                    type: "shadow", // 'shadow' as default; can also be 'line' or 'shadow'
                },
            },
            title: {
                text: `前 ${categories.length} 职业学历需求堆叠条形图`,
                left: "center",
            },
            legend: {
                top: "bottom",
            },
            grid: {
                top: "5%",
                left: "3%",
                right: "4%",
                bottom: "6%",
                containLabel: true,
            },
            xAxis: {
                type: "value",
            },
            yAxis: {
                type: "category",
                data: categories,
            },
            series: Object.keys(categoryDegreeData[categories[0]]).map((degree) => {
                return {
                    name: degree,
                    type: "bar",
                    stack: "all",
                    emphasis: {
                        focus: "series",
                    },
                    data: categories.map((category) => {
                        return categoryDegreeData[category][degree];
                    }),
                };
            }),
        });
    }
    // 学历分析结束

    // 经验分析
    function renderExperiencePieChart(data) {
        experiencePieChart.clear();
        const experienceData = data["experienceProportion"];
        experiencePieChart.setOption({
            title: {
                text: `所有职业经验占比`,
                left: "center",
            },
            legend: {
                top: "bottom",
            },
            tooltip: {
                trigger: "item",
            },
            series: [
                {
                    name: "Access From",
                    type: "pie",
                    radius: ["40%", "70%"],
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: "#fff",
                        borderWidth: 2,
                    },
                    label: {
                        show: false,
                        position: "center",
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: "40",
                            fontWeight: "bold",
                        },
                    },
                    labelLine: {
                        show: false,
                    },
                    data: Object.keys(experienceData).map((key) => {
                        return {
                            name: key,
                            value: experienceData[key],
                        };
                    }),
                },
            ],
        });
    }

    function renderExperienceBarChart(data) {
        experienceBarChart.clear();
        const categoryExperienceData = data["categoryExperienceProportion"];
        const categories = Object.keys(categoryExperienceData);
        experienceBarChart.setOption({
            tooltip: {
                trigger: "axis",
                axisPointer: {
                    // Use axis to trigger tooltip
                    type: "shadow", // 'shadow' as default; can also be 'line' or 'shadow'
                },
            },
            title: {
                text: `前 ${categories.length} 职业经验需求堆叠条形图`,
                left: "center",
            },
            legend: {
                top: "bottom",
            },
            grid: {
                top: "5%",
                left: "3%",
                right: "4%",
                bottom: "6%",
                containLabel: true,
            },
            xAxis: {
                type: "value",
            },
            yAxis: {
                type: "category",
                data: categories,
            },
            series: Object.keys(categoryExperienceData[categories[0]]).map((experience) => {
                return {
                    name: experience,
                    type: "bar",
                    stack: "all",
                    emphasis: {
                        focus: "series",
                    },
                    data: categories.map((category) => {
                        return categoryExperienceData[category][experience];
                    }),
                };
            }),
        });
    }
    // 经验分析结束

    window.onload = () => {
        form.onsubmit();
    };

    window.onresize = () => {
        if (data) {
            salaryBarChart.resize();
            groupPieChart.resize();
            degreePieChart.resize();
            degreeBarChart.resize();
            experiencePieChart.resize();
            experienceBarChart.resize();
        }
    };
});
