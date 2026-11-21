let chart;
async function refreshDashboard(){
 const response=await fetch('/api/metrics');const rows=await response.json();if(!rows.length)return;
 const latest=rows[rows.length-1];
 [['cpu',latest.cpu],['memory',latest.memory],['disk',latest.disk]].forEach(([k,v])=>{document.getElementById(k+'Value').textContent=v.toFixed(1)+'%';document.getElementById(k+'Bar').style.width=v+'%';});
 document.getElementById('processValue').textContent=latest.process_count;
 const high=latest.cpu>=80||latest.memory>=85||latest.disk>=90;
 document.getElementById('healthStatus').textContent=high?'Attention required':'All systems operational';
 document.getElementById('healthText').textContent=high?'A resource crossed its configured warning threshold.':'Current resource usage is within configured thresholds.';
 document.getElementById('recentRows').innerHTML=rows.slice(-7).reverse().map(r=>`<tr><td>${new Date(r.timestamp).toLocaleTimeString()}</td><td>${r.cpu.toFixed(1)}%</td><td>${r.memory.toFixed(1)}%</td><td>${r.disk.toFixed(1)}%</td><td>${r.process_count}</td></tr>`).join('');
 const labels=rows.map(r=>new Date(r.timestamp).toLocaleTimeString());
 const datasets=[['CPU','cpu'],['Memory','memory'],['Disk','disk']].map(([label,k])=>({label,data:rows.map(r=>r[k]),tension:.35,borderWidth:2,pointRadius:0}));
 if(!chart)chart=new Chart(document.getElementById('resourceChart'),{type:'line',data:{labels,datasets},options:{responsive:true,plugins:{legend:{labels:{color:'#aebbd0'}}},scales:{x:{ticks:{color:'#8795aa',maxTicksLimit:8},grid:{color:'#263449'}},y:{min:0,max:100,ticks:{color:'#8795aa'},grid:{color:'#263449'}}}}});
 else{chart.data.labels=labels;chart.data.datasets.forEach((d,i)=>d.data=datasets[i].data);chart.update();}
}
refreshDashboard();setInterval(refreshDashboard,5000);
