import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.metrics import r2_score
import json
from tethysapp.tethysdash.plugin_helpers import TethysDashPlugin


class MachineLearning(TethysDashPlugin):
    name = "machine_learning"
    args = {
        "model_type": [
            "linear_regression",
            "decision_tree",
            "random_forest",
            "knn",
            "svr",
        ]
    }
    group = "Machine Learning"
    label = "Simple ML Model Demo"
    type = "plotly"
    tags = ["machine_learning", "plotly", "impact", "statements"]
    description = "An plugin showing an example of a machine learning model output"

    def run(self):
        """
        Demonstrate a simple ML model interactively using Plotly.

        model_type: str
            "linear_regression" or "decision_tree"
        """
        # 1️⃣ Create synthetic data: y = 2x + 1 + noise
        X = np.linspace(0, 10, 20).reshape(-1, 1)
        y = 2 * X.squeeze() + 1 + np.random.randn(20)

        # 2️⃣ Select model
        model_map = {
            "linear_regression": (LinearRegression(), "Linear Regression"),
            "decision_tree": (DecisionTreeRegressor(max_depth=3), "Decision Tree"),
            "random_forest": (
                RandomForestRegressor(n_estimators=50, random_state=0),
                "Random Forest",
            ),
            "knn": (KNeighborsRegressor(n_neighbors=3), "K-Nearest Neighbors"),
            "svr": (SVR(kernel="rbf"), "Support Vector Regression"),
        }

        if self.model_type not in model_map:
            raise ValueError(
                f"Unknown model_type '{self.model_type}'. Choose from: {list(model_map.keys())}"
            )

        model, model_name = model_map[self.model_type]
        model.fit(X, y)

        # 3️⃣ Make predictions
        X_test = np.linspace(0, 10, 200).reshape(-1, 1)
        y_pred = model.predict(X_test)

        # 4️⃣ Compute R² score
        r2 = r2_score(y, model.predict(X))

        # 5️⃣ Create interactive Plotly figure
        fig = go.Figure()

        # Training data
        fig.add_trace(
            go.Scatter(
                x=X.squeeze(),
                y=y,
                mode="markers",
                name="Training data",
                marker=dict(size=8, color="blue", opacity=0.7),
            )
        )

        # Model prediction
        fig.add_trace(
            go.Scatter(
                x=X_test.squeeze(),
                y=y_pred,
                mode="lines",
                name=f"{model_name} prediction",
                line=dict(color="red", width=3),
            )
        )

        # 6️⃣ Build annotation list
        annotations = [
            dict(
                x=0.02,
                y=0.98,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text=f"<b>Model:</b> {model_name}<br><b>R² =</b> {r2:.3f}",
                showarrow=False,
                font=dict(size=14, color="black"),
                bgcolor="rgba(255,255,255,0.8)",
                bordercolor="gray",
                borderwidth=1,
            )
        ]

        # If linear model, show equation
        if hasattr(model, "coef_"):
            slope = model.coef_[0]
            intercept = model.intercept_
            annotations.append(
                dict(
                    x=0.02,
                    y=0.8,
                    xref="paper",
                    yref="paper",
                    xanchor="left",
                    yanchor="top",
                    text=f"<b>y = {slope:.2f}x + {intercept:.2f}</b>",
                    showarrow=False,
                    font=dict(size=14, color="black"),
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="gray",
                    borderwidth=1,
                )
            )

        # 7️⃣ Style and layout
        fig.update_layout(
            title=f"{model_name} Regression Demo",
            xaxis_title="X",
            yaxis_title="y",
            template="plotly_white",
            annotations=annotations,
        )

        return json.loads(fig.to_json())
