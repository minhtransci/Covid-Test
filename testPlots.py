import plotly.express as px
import plotly.graph_objects as go
import decimal as d

tmp = d.Decimal('1.357')
print(tmp)

fig = go.Figure()


fig.add_trace(go.Scatter(x=[-3, -2.5, -2, -1.5, -1, -0.5, 0],
                         y=[d.Decimal('0.026132407407407406'),d.Decimal('0.012072222222222222'),d.Decimal('0.004334907407407407'),d.Decimal('0.001298888888888889'),d.Decimal('0.0003400925925925926'),d.Decimal('0.0003400925925925926'),d.Decimal('3.26099537037037e-05')],
                    mode='lines+markers', name='Train (-3,-2.5,-2,-1.5,-1,-0.5,0)', marker=dict(size=16)))

fig.add_trace(go.Scatter(x=[-3, -2.5, -2, -1.5, -1, -0.5, 0],
                         y=[d.Decimal('0.026906296296296296'),d.Decimal('0.013908055555555555'),d.Decimal('0.006337314814814815'),d.Decimal('0.002905'),d.Decimal('0.0014596296296296297'),d.Decimal('0.0009818518518518518'),d.Decimal('0.0008256481481481482')],
                    mode='lines+markers', name='Train (-3)', marker=dict(size=16)))

fig.add_trace(go.Scatter(x=[-3, -2.5, -2, -1.5, -1, -0.5, 0],
                         y=[d.Decimal('0.0300725'),d.Decimal('0.013783518518518518'),d.Decimal('0.004506388888888889'),d.Decimal('0.0011442592592592594'),d.Decimal('0.00023851851851851852'),d.Decimal('5e-05'),d.Decimal('8.904649330181246e-06')],
                    mode='lines+markers', name='Train (0)', marker=dict(size=16)))



fig.add_trace(go.Scatter(x=[0, 0.5, 1, 1.5, 2, 2.5, 3],
                         y=[d.Decimal('0.05217472222222222'),d.Decimal('0.030999537037037037'),d.Decimal('0.013505462962962962'),d.Decimal('0.0036874074074074075'),d.Decimal('0.0005035185185185185'),d.Decimal('3.1512345679012344e-05'),d.Decimal('1.7237982663514579e-06')],
                    mode='lines+markers', name='Train (0,0.5,1,1.5,2,2.5,3)', marker=dict(size=16)))

fig.add_trace(go.Scatter(x=[0, 0.5, 1, 1.5, 2, 2.5, 3],
                         y=[d.Decimal('0.07920222222222222'),d.Decimal('0.06151398148148148'),d.Decimal('0.03880898148148148'),d.Decimal('0.017549444444444444'),d.Decimal('0.006756111111111111'),d.Decimal('0.003717222222222222'),d.Decimal('0.003078888888888889')],
                    mode='lines+markers', name='Train (0)', marker=dict(size=16)))

fig.add_trace(go.Scatter(x=[0, 0.5, 1, 1.5, 2, 2.5, 3],
                         y=[d.Decimal('0.06499546296296296'),d.Decimal('0.048294166666666666'),d.Decimal('0.028417777777777778'),d.Decimal('0.008876574074074075'),d.Decimal('0.001071111111111111'),d.Decimal('5.977366255144033e-05'),d.Decimal('3.3983451536643025e-06')],
                    mode='lines+markers', name='Train (3)', marker=dict(size=16)))

fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
))


fig.update_yaxes(type="log")
fig.show()