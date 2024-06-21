from .models import (
    Templates,
    Types,
    Inputs,
    Template_users_logins,
    Template_users_accounts,
    Template_developers_logins,
    Template_developers_accounts,
)


def insert_data():
    user_logins = ["johnny", "alice", "bob", "emily"]
    dev_logins = ["sam_dev", "sophia_dev", "max_dev", "lucydev"]

    user_accounts = ["@biology", "@chemistry", "@physics", "@geology"]
    dev_accounts = ["@ai", "@robotics", "@iot", "@data-science"]

    template1, _ = Templates.get_or_create(
        name="Distributed matrix computation", description="Multiply matrix with MPI"
    )
    template2, _ = Templates.get_or_create(
        name="AI-based solving", description="Solve a complex problem with AI"
    )
    template3, _ = Templates.get_or_create(
        name="Real-time weather simulation",
        description="Simulate weather patterns using real-time data and predictive models",
    )

    type_float, _ = Types.get_or_create(name="float")
    type_string, _ = Types.get_or_create(name="string")
    type_int, _ = Types.get_or_create(name="int")

    # input template1
    input1_t1, _ = Inputs.get_or_create(
        name="Matrix Size",
        description="Size of the matrix (NxN)",
        default="1000",
        minVal=1.0,
        maxVal=10000.0,
        regex=None,
        template=1,
        type=type_float,
    )

    input2_t1, _ = Inputs.get_or_create(
        name="Computation Timeout",
        description="Maximum computation time in seconds",
        default="60.0",
        minVal=None,
        maxVal=None,
        regex=None,
        template=1,
        type=type_float,
    )

    input3_t1, _ = Inputs.get_or_create(
        name="Matrix File Path",
        description="Path to the input matrix file",
        default="",
        minVal=None,
        maxVal=None,
        regex="^\/[a-zA-Z0-9_\-\/]+$",
        template=1,
        type=type_string,
    )

    input4_t1, _ = Inputs.get_or_create(
        name="Output Directory",
        description="Directory to save the computation results",
        default="",
        minVal=None,
        maxVal=None,
        regex=None,
        template=1,
        type=type_string,
    )

    # input template2
    input1_t2, _ = Inputs.get_or_create(
        name="Training Iterations",
        description="Number of training iterations for the AI model",
        default="100",
        minVal=1.0,
        maxVal=10000.0,
        regex=None,
        template=template2,
        type=type_float,
    )

    input2_t2, _ = Inputs.get_or_create(
        name="Learning Rate",
        description="Learning rate for the AI model training",
        default="0.01",
        minVal=None,
        maxVal=None,
        regex=None,
        template=template2,
        type=type_float,
    )

    input3_t2, _ = Inputs.get_or_create(
        name="Model Save Path",
        description="Path to save the trained AI model",
        default="",
        minVal=None,
        maxVal=None,
        regex="^\/[a-zA-Z0-9_\-\/]+$",
        template=template2,
        type=type_string,
    )

    input4_t2, _ = Inputs.get_or_create(
        name="Dataset Directory",
        description="Directory containing the training dataset",
        default="",
        minVal=None,
        maxVal=None,
        regex=None,
        template=template2,
        type=type_string,
    )

    # input template3
    input1_t3, _ = Inputs.get_or_create(
        name="Simulation Duration",
        description="Duration of the weather simulation in hours",
        default="24",
        minVal=1.0,
        maxVal=168.0,
        regex=None,
        template=template3,
        type=type_float,
    )

    input2_t3, _ = Inputs.get_or_create(
        name="Update Interval",
        description="Interval in minutes for updating simulation data",
        default="10.0",
        minVal=None,
        maxVal=None,
        regex=None,
        template=template3,
        type=type_float,
    )

    input3_t3, _ = Inputs.get_or_create(
        name="Location Identifier",
        description="Identifier for the location of the simulation",
        default="",
        minVal=None,
        maxVal=None,
        regex="^[a-zA-Z0-9_\-]+$",
        template=template3,
        type=type_string,
    )

    input4_t3, _ = Inputs.get_or_create(
        name="Data Source",
        description="Source of the real-time data for the simulation",
        default="",
        minVal=None,
        maxVal=None,
        regex=None,
        template=template3,
        type=type_string,
    )

    # Génération des logins et comptes pour template1
    for i in range(4):
        Template_users_logins.create(name=user_logins[i], template=template1)
        Template_users_accounts.create(name=user_accounts[i], template=template1)
        Template_developers_logins.create(name=dev_logins[i], template=template1)
        Template_developers_accounts.create(name=dev_accounts[i], template=template1)

    # Génération des logins et comptes pour template2
    for i in range(4):
        Template_users_logins.create(name=user_logins[i], template=template2)
        Template_users_accounts.create(name=user_accounts[i], template=template2)
        Template_developers_logins.create(name=dev_logins[i], template=template2)
        Template_developers_accounts.create(name=dev_accounts[i], template=template2)

    # Génération des logins et comptes pour template3
    for i in range(4):
        Template_users_logins.create(name=user_logins[i], template=template3)
        Template_users_accounts.create(name=user_accounts[i], template=template3)
        Template_developers_logins.create(name=dev_logins[i], template=template3)
        Template_developers_accounts.create(name=dev_accounts[i], template=template3)
