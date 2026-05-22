class TPerson : public TObject {
public:
    TPerson();
    virtual void Save();
    int Age;

private:
    char* Name;
};
