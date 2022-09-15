document.addEventListener("DOMContentLoaded", () => {
    var data = null;
    var tableRenderer;
    var first = true;
    const salaryBarChart = echarts.init(document.getElementById("salaryBar"));
    const salaryPieChart = echarts.init(document.getElementById("salaryPie"));

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
            success: (result) => {
                data = JSON.parse(result);
                renderSalaryChart(data);
                renderDegreeChart(data);
                renderExperienceChart(data);
            },
            error: (_xhr, _status, _error) => {
                window.alert(_error);
            },
        });
        return false;
    };

    function renderSalaryChart(data) {
        salaryBarChart.clear();
        const salaryData = data["salaryIntervalProportion"];
        salaryBarChart.setOption({
            title: {
                text: `当前职业薪水分布图`,
                left: "center",
            },
            xAxis: {
                type: "category",
                data: Object.keys(salaryData),
            },
            yAxis: {
                type: "value",
            },
            series: [
                {
                    data: Object.values(salaryData),
                    type: "bar",
                },
            ],
        });

        salaryPieChart.clear();
        salaryPieChart.setOption({
            title: {
                text: `当前职业所需学历占比`,
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
                    data: Object.keys(salaryData).map((key) => {
                        return {
                            name: key,
                            value: salaryData[key],
                        };
                    }),
                },
            ],
        });
    }

    // 学历分析
    function renderDegreeChart(data) {
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

        degreeBarChart.setOption({
            title: {
                text: `当前职业薪水分布图`,
                left: "center",
            },
            xAxis: {
                type: "category",
                data: Object.keys(degreeData),
            },
            yAxis: {
                type: "value",
            },
            series: [
                {
                    data: Object.values(degreeData),
                    type: "bar",
                },
            ],
        });
    }
    // 学历分析结束

    // 经验分析
    function renderExperienceChart(data) {
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

        experienceBarChart.clear();
        experienceBarChart.setOption({
            title: {
                text: `当前职业薪水分布图`,
                left: "center",
            },
            xAxis: {
                type: "category",
                data: Object.keys(experienceData),
            },
            yAxis: {
                type: "value",
            },
            series: [
                {
                    data: Object.values(experienceData),
                    type: "bar",
                },
            ],
        });
    }
    // 经验分析结束

    window.onload = () => {
        form.onsubmit();
    };

    window.onresize = () => {
        if (data) {
            salaryBarChart.resize();
            salaryPieChart.resize();
            degreePieChart.resize();
            degreeBarChart.resize();
            experiencePieChart.resize();
            experienceBarChart.resize();
        }
    };
});
